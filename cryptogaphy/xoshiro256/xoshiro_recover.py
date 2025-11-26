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
        pass

    def reverse_state(self, output):
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
        s0 = self._reverse_s0(s1_prev, s1, s2)
        new_state.s0 = s0

        # 4. to recover s3 we need s0 in at least 2 states in a row
        if self.prng_states[self.current_state-1].s0 == 0:
            self.prng_states.append(new_state)
            self.current_state += 1
            return

        s0_prev = self.prng_states[self.current_state-1].s0
        s3 = self._reverse_s3(s0, s0_prev)
        new_state.s3 = s3
        self.prng_states.append(new_state)
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

    def _reverse_s3(self, s0_prev, s0):
        s3 = self._rotr(s0_prev ^ s0, 45)
        return s3


if __name__ == '__main__':
    xoshiro256 = Xoshiro256(10804161907448682703, 11460624974815451986, 15774960471522575440, 15521138194195770664)
    xoshiro256_recover = Xoshiro256Recover()
    output1 = xoshiro256.next_uint64()
    xoshiro256_recover.reverse_state(output1)
    output2 = xoshiro256.next_uint64()
    xoshiro256_recover.reverse_state(output2)
    output3 = xoshiro256.next_uint64()
    xoshiro256_recover.reverse_state(output3)
    output4 = xoshiro256.next_uint64()
    xoshiro256_recover.reverse_state(output4)
    output5 = xoshiro256.next_uint64()
    xoshiro256_recover.reverse_state(output5)
