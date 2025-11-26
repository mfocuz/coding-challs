from cryptogaphy.xoshiro256.xoshiro256 import Xoshiro256State
from xoshiro256 import Xoshiro256
from xoshiro256 import Xoshiro256Base

class Xoshiro256Recover(Xoshiro256Base):
    BIT64 = 0xffffffffffffffff
    INV_9 = 0x8e38e38e38e38e39 # 9 * INV_9 ≡ 1 (mod 2^64)
    INV_5 = 0xcccccccccccccccd # 5 * INV_5 ≡ 1 (mod 2^64)

    current_state = 0
    prng_states = []

    def __init__(self):
        self.current_state = 0
        self.prng_states = []

    def check_if_state_recovered(self):
        for i in self.prng_states:
            if i.s0 != 0 and i.s1 != 0 and i.s2 != 0 and i.s3 != 0:
                return i.s0, i.s1, i.s2, i.s3

        return None

    def reverse_state(self, output):
        recovered_state = self.check_if_state_recovered()
        if recovered_state is not None:
            return recovered_state

        new_state = Xoshiro256State(0, 0, 0, 0)

        # 1. recover s1 of current state
        s1 = self._reverse_s1(output)
        new_state.s1 = s1

        # we need minimal 3 values to recover state from full 64bit output
        if len(self.prng_states) < 2:
            self.prng_states.append(new_state)
            self.current_state += 1
            return

        # 2. to recover s2 we need at least 2 prev states, and will recover s2 for current_state-1
        s1_prev = self.prng_states[self.current_state-1].s1
        s2 = self._reverse_s2(s1_prev, s1)
        new_state.s2 = s2

        # 3. to recover s0 we need s2 in previous state
        if self.prng_states[self.current_state-1].s2 == 0:
            self.prng_states.append(new_state)
            self.current_state += 1
            return

        s2_prev = self.prng_states[self.current_state-1].s2
        s0_prev = self._reverse_s0(s1, s1_prev, s2_prev)
        self.prng_states[self.current_state - 1].s0 = s0_prev

        # 4. to recover s3 we need s0 in at least 2 states in a row
        if self.prng_states[self.current_state-1].s0 == 0 or self.prng_states[self.current_state-2].s0 == 0:
            self.prng_states.append(new_state)
            self.current_state += 1
            return

        s0_prev_prev = self.prng_states[self.current_state-2].s0
        s1_prev_prev = self.prng_states[self.current_state-2].s1
        s3 = self._reverse_s3(s0_prev_prev, s1_prev_prev, s0_prev)
        self.prng_states[self.current_state-2].s3 = s3
        self.current_state += 1

    def generate(self):
        return self.xoshiro256.next_uint64()

    def _reverse_s0(self, s1, s1_prev, s2_prev):
        s0 = s1 ^ s1_prev ^ s2_prev
        return s0

    def _reverse_s1(self, output_value):
        r2 = output_value * self.INV_9 & self.BIT64
        r1 = self._rotr(r2, 7)
        s1 = r1 * self.INV_5 & self.BIT64
        return s1

    def _reverse_s2(self, s1_n_prev, s1_n):
        n3 = s1_n ^ s1_n_prev
        n2 = s1_n_prev << 17 & self.BIT64
        s2 = n3 ^ n2
        return s2

    def _reverse_s3(self, s0_prev,  s1_prev, s0):
        s3 = s0_prev ^ s0 ^ s1_prev
        return s3


if __name__ == '__main__':
    xoshiro256 = Xoshiro256(10804161907448682703, 11460624974815451986, 15774960471522575440, 15521138194195770664)
    xoshiro256_recover = Xoshiro256Recover()

    i = 0
    while True:
        print ("output iteration: %i" % i)
        output = xoshiro256.next_uint64()
        state = xoshiro256_recover.reverse_state(output)
        i += 1
        if state is not None:
            break

    xoshiro256 = Xoshiro256(state[0], state[1], state[2], state[3])
    for i in range(20):
        value = xoshiro256.generate()
        print("i:%i, 64bit: %s, 32bit:%s" % (i, value, value >> 32))

