import time

from z3 import BitVec, BitVecVal, Or, RotateLeft, Solver, ZeroExt, sat

from xoshiro256 import Xoshiro256


"""
One-step SMT model for recovering the initial xoshiro256** state from outputs.

This file applies the recommendation:

    **Give Z3 only independent variables + one step of transition.**

Instead of building a symbolic chain:

    s[i+1] = f(s[i])
    s[i+2] = f(f(s[i]))
    s[i+3] = f(f(f(s[i])))

we do:

    - Make the state at t = 0 symbolic (s0_0, s1_0, s2_0, s3_0).
    - Constrain ONLY the first output (outputs[0]) using the xoshiro256**
      non-linear output function inside Z3.
    - Ask Z3 for a model (a candidate initial state).
    - Run a real Xoshiro256 instance in Python from that candidate state and
      check all remaining outputs concretely (no more SMT).
    - If the concrete sequence does not match, block that model and ask Z3
      for another model.

This way Z3 never has to propagate the non-linear multiplications and rotates
across many time steps; it only sees a single call to the transition/output
function, which drastically reduces the complexity of the SMT problem.

The next recommendations are applied as follows:

    **Break the nonlinear part out of the recursion**
    **Manually invert what is invertible**

All non-linear and invertible operations (multiplication by odd constants,
bit-rotations, masking) are evaluated *concretely in Python* whenever the
inputs are known, instead of being pushed into Z3. The SMT model only
handles the truly unknown bits at the very first step.
"""


BIT64 = 0xFFFFFFFFFFFFFFFF


def _step_transition_python(s0, s1, s2, s3):
    """
    Pure-Python copy of xoshiro256** state transition, WITHOUT the non-linear
    output part. This matches Xoshiro256.generate()'s state update.
    """
    n2 = (s1 << 17) & BIT64
    n3 = s2 ^ s0
    n4 = s3 ^ s1
    s1_next = s1 ^ n3
    s0_next = s0 ^ n4
    s2_next = n3 ^ n2

    # rotl(n4, 45)
    x1 = (n4 << 45) & BIT64
    x2 = (n4 >> (64 - 45)) & BIT64
    s3_next = (x1 | x2) & BIT64

    return s0_next, s1_next, s2_next, s3_next


def verify_candidate_by_step_smt(cand_s0, cand_s1, cand_s2, cand_s3, outputs):
    """
    Apply the "break nonlinear part out of recursion" and
    "manually invert what is invertible" pattern.

    Once the initial state is concrete, there are *no unknowns* left in the
    later steps, so we do not need SMT there at all:

        - we evolve the state in pure Python (non-recursive unrolling),
        - we compute the non-linear output function in Python,
        - we only compare the high 32 bits to the observed outputs.

    This keeps **all** nonlinear work (mul by 5, rotl 7, mul by 9) out of Z3.
    """
    state = (cand_s0, cand_s1, cand_s2, cand_s3)

    for idx, expected in enumerate(outputs):
        s0_val, s1_val, s2_val, s3_val = state

        # Nonlinear output function evaluated concretely in Python:
        # n1 = ((s1 * 5) <<< 7) * 9  (mod 2^64)
        r1 = (s1_val * 5) & BIT64
        # rotl(r1, 7)
        rot = ((r1 << 7) & BIT64) | (r1 >> (64 - 7))
        n1 = (rot * 9) & BIT64
        high32 = (n1 >> 32) & 0xFFFFFFFF

        if high32 != expected:
            print(
                f"per-step check failed at sample {idx}: "
                f"expected {expected}, got {high32}"
            )
            return False

        # Advance to next *actual* state purely in Python.
        state = _step_transition_python(s0_val, s1_val, s2_val, s3_val)

    return True


def recover_s1_from_outputs_onestep(outputs):
    """
    Recover the initial xoshiro256** state from a sequence of 32‑bit outputs,
    using Z3 for ONLY ONE nonlinear step and verifying the rest by simulation.

    :param outputs: list of uint32 values (high 32 bits of xoshiro256** output)
    :return: (s0, s1, s2, s3) or None if no state matches the outputs
    """

    if not outputs:
        return None

    solver = Solver()

    # Symbolic state only at t = 0
    s0_0 = BitVec("s0_0", 64)
    s1_0 = BitVec("s1_0", 64)
    s2_0 = BitVec("s2_0", 64)
    s3_0 = BitVec("s3_0", 64)

    # We only use the very first output in the SMT constraints.
    u0 = BitVecVal(outputs[0], 32)
    low0 = BitVec("low_0", 32)  # unknown low 32 bits of n1 at t = 0

    # Full 64-bit output at t=0: upper 32 bits are known (u0), lower 32 bits symbolic.
    n1_0 = BitVec("n1_0", 64)
    solver.add(n1_0 == (ZeroExt(32, u0) << 32) | ZeroExt(32, low0))

    # xoshiro256** output function for ONE step:
    # n1_state_0 = ((s1_0 * 5) <<< 7) * 9  (mod 2^64)
    r1_0 = s1_0 * BitVecVal(5, 64)
    r2_0 = RotateLeft(r1_0, 7)
    n1_state_0 = r2_0 * BitVecVal(9, 64)

    solver.add(n1_state_0 == n1_0)

    print("assertions (one-step model):", len(solver.assertions()))

    # Enumerate candidate states that satisfy the first-output constraint and
    # keep the first one that matches the entire observed sequence.
    while True:
        result = solver.check()
        print("solver.check() ->", result)
        if result != sat:
            # No more states consistent with outputs[0]
            return None

        # Some variables (e.g. s0_0, s2_0, s3_0) may be unconstrained by the
        # one-step equation and thus absent from the model. Use model_completion=True
        # so Z3 picks *some* consistent value for them.
        model = solver.model()
        cand_s0 = model.eval(s0_0, model_completion=True).as_long()
        cand_s1 = model.eval(s1_0, model_completion=True).as_long()
        cand_s2 = model.eval(s2_0, model_completion=True).as_long()
        cand_s3 = model.eval(s3_0, model_completion=True).as_long()

        print("candidate state s0..s3 at t=0 (from first-step SMT):")
        print("  s0_0:", cand_s0)
        print("  s1_0:", cand_s1)
        print("  s2_0:", cand_s2)
        print("  s3_0:", cand_s3)

        # Verification using the "per-sample one-step SMT" pattern.
        ok = verify_candidate_by_step_smt(cand_s0, cand_s1, cand_s2, cand_s3, outputs)

        if ok:
            print("recovered state s0..s3 at t=0 (verified against all outputs):")
            print("  s0_0:", cand_s0)
            print("  s1_0:", cand_s1)
            print("  s2_0:", cand_s2)
            print("  s3_0:", cand_s3)
            return cand_s0, cand_s1, cand_s2, cand_s3

        # Block this exact 256-bit state so that Z3 finds a different model.
        solver.add(
            Or(
                s0_0 != BitVecVal(cand_s0, 64),
                s1_0 != BitVecVal(cand_s1, 64),
                s2_0 != BitVecVal(cand_s2, 64),
                s3_0 != BitVecVal(cand_s3, 64),
            )
        )


if __name__ == "__main__":
    # Small demo to show the one-step model in action.
    xoshiro1 = Xoshiro256(
        10804161907448682703,
        11460624974815451986,
        15774960471522575440,
        15521138194195770664,
    )
    print("Original sequence (first 15 uint32):")
    original = []
    for _ in range(15):
        v = xoshiro1.next_uint32()
        original.append(v)
        print(v)

    print("\nRecovering state from first 8 outputs:")
    xoshiro2 = Xoshiro256(
        10804161907448682703,
        11460624974815451986,
        15774960471522575440,
        15521138194195770664,
    )
    observed = [xoshiro2.next_uint32() for _ in range(8)]

    t0 = time.time()
    print("Observed outputs:", observed)
    recovered = recover_s1_from_outputs_onestep(observed)
    print("done, recovered state:", recovered)
    t1 = time.time()
    print("solver time:", t1 - t0, "seconds")

    if recovered is not None:
        print("\nReconstructed sequence from recovered state (first 15 uint32):")
        xoshiro_recovered = Xoshiro256(*recovered)
        for _ in range(15):
            print(xoshiro_recovered.next_uint32())


