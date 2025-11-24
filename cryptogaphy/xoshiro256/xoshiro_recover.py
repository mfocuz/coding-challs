from xoshiro256 import Xoshiro256
from xoshiro256 import Xoshiro256Base

class Xoshiro256Recover(Xoshiro256Base):
    s0 = s1 = s2 = s3 = 0
    s0_prev = s1_prev = s2_prev = s3_prev = 0
    r1 = r2 = 0
    n1 = n2 = n3 = n4 = n5 = n6 = n7 = n8 = 0

    INV_9 = 0x8e38e38e38e38e39 # 9 * INV_9 ≡ 1 (mod 2^64)
    INV_5 = 0xcccccccccccccccd # 5 * INV_5 ≡ 1 (mod 2^64)
    xoshiro256 = None

    def __init__(self, known_output1, known_output2):
        self.reverse_state(known_output1, known_output2)

    def reverse_state(self, known_output1, known_output2):
        # recover s1_old
        self.r2 = known_output1 * self.INV_9 & 0xffffffffffffffff
        self.r1 = self._rotr(self.r2, 7)
        self.s1_prev = self.r1 * self.INV_5 & 0xffffffffffffffff

        # recover s1_new
        self.r2 = known_output2 * self.INV_9 & 0xffffffffffffffff
        self.r1 = self._rotr(self.r2, 7)
        self.s1 = self.r1 * self.INV_5 & 0xffffffffffffffff

        # recover intermediate
        self.n3 = self.s1_prev ^ self.s1
        self.n2 = self.s1_prev << 17 & 0xffffffffffffffff
        self.s2 = self.n3 ^ self.n2
    
    def reverse_s1(self, value):
        r2 = value * self.INV_9 & 0xffffffffffffffff
        r1 = self._rotr(r2, 7)
        s1 = r1 * self.INV_5 & 0xffffffffffffffff
        return s1










if __name__ == '__main__':
    xoshiro256 = Xoshiro256(10804161907448682703, 11460624974815451986, 15774960471522575440, 15521138194195770664)
    output1 = xoshiro256.next_uint64()
    output2 = xoshiro256.next_uint64()
    print(f"Output x64bit: {output1}")
    xoshiro256_recover = Xoshiro256Recover(output1, output2)

    first_value = xoshiro256.next_uint32()