import time

from z3 import BitVec, BitVecVal, Solver, ZeroExt, RotateLeft, sat

from cryptogaphy.xoshiro256.xoshiro_recover import Xoshiro256Recover
from xoshiro256 import Xoshiro256


def recover_s1_from_outputs(outputs):
    t_count = len(outputs)
    s0 = [BitVec(f"s0_{i}", 64) for i in range(t_count + 1)]
    s1 = [BitVec(f"s1_{i}", 64) for i in range(t_count + 1)]
    s2 = [BitVec(f"s2_{i}", 64) for i in range(t_count + 1)]
    s3 = [BitVec(f"s3_{i}", 64) for i in range(t_count + 1)]
    low = [BitVec(f"low_{i}", 32) for i in range(t_count)]
    solver = Solver()
    for i in range(t_count):
        u = BitVecVal(outputs[i], 32)
        n1 = BitVec(f"n1_{i}", 64)
        solver.add(n1 == (ZeroExt(32, u) << 32) | ZeroExt(32, low[i]))
        r1 = s1[i] * BitVecVal(5, 64)
        r2 = RotateLeft(r1, 7)
        n1_state = r2 * BitVecVal(9, 64)
        solver.add(n1_state == n1)
        n2 = s1[i] << 17
        n3 = s2[i] ^ s0[i]
        n4 = s3[i] ^ s1[i]
        s1_next = s1[i] ^ n3
        s0_next = s0[i] ^ n4
        s2_next = n3 ^ n2
        s3_next = RotateLeft(n4, 45)
        solver.add(s0[i + 1] == s0_next)
        solver.add(s1[i + 1] == s1_next)
        solver.add(s2[i + 1] == s2_next)
        solver.add(s3[i + 1] == s3_next)
    print("assertions:", len(solver.assertions()))
    result = solver.check()
    print("solver.check() ->", result)
    if result != sat:
        return None
    model = solver.model()
    recovered_s0 = model[s0[0]].as_long()
    recovered_s1 = model[s1[0]].as_long()
    recovered_s2 = model[s2[0]].as_long()
    recovered_s3 = model[s3[0]].as_long()
    print("recovered state s0..s3 at t=0:")
    print("  s0[0]:", recovered_s0)
    print("  s1[0]:", recovered_s1)
    print("  s2[0]:", recovered_s2)
    print("  s3[0]:", recovered_s3)
    return recovered_s0, recovered_s1, recovered_s2, recovered_s3


if __name__ == "__main__":
    # Basic
    xoshiro1 = Xoshiro256(
        10804161907448682703,
        11460624974815451986,
        15774960471522575440,
        15521138194195770664,
    )
    outputs = []
    print("Original Sequence")
    for _ in range(15):
        val32 = xoshiro1.next_uint32()
        print(val32)

    print("Recovering s1 from outputs:")
    outputs = []
    xoshiro2 = Xoshiro256(
        10804161907448682703,
        11460624974815451986,
        15774960471522575440,
        15521138194195770664,
    )
    for _ in range(8):
        val32 = xoshiro2.next_uint32()
        outputs.append(val32)
    t0 = time.time()
    print("32-bit outputs (high 32 bits of n1):", outputs)
    recovered = recover_s1_from_outputs(outputs)
    print("done, recovered state:", recovered)
    t1 = time.time()
    print("solver time:", t1 - t0, "seconds")

    print("Reconstructed sequence:")
    xoshiro_recovered = Xoshiro256(recovered[0], recovered[1], recovered[2], recovered[3])
    for _ in range(15):
        val32 = xoshiro_recovered.next_uint32()
        print(val32)



