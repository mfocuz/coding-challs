

class Xoshiro256:
    bit64 = 0xffffffffffffffff
    s0 = s1 = s2 = s3 = 0
    n1 = n2 = n3 = n4 = n5 = n6 = n7 = n8 = 0
    r1 = r2 = r3 = 0

    def __init__(self, s0, s1, s2, s3):
        """Initialize with 4 64-bit integers as state values."""
        self.s0 = s0 & 0xffffffffffffffff
        self.s1 = s1 & 0xffffffffffffffff
        self.s2 = s2 & 0xffffffffffffffff
        self.s3 = s3 & 0xffffffffffffffff
        self.state = [self.s0, self.s1, self.s2, self.s3]
        self.n1 = self.n2 = self.n3 = self.n4 = self.n5 = self.n6 = self.n7 = self.n8 = 0
        self.intermediate_state = [self.n1, self.n2, self.n3, self.n4, self.n5, self.n6, self.n7, self.n8]

    def print_state(self):
        print(f"Xoshiro256 current state:")
        for i in self.state:
            print(f"  state[{i}] = 0x{self.state[i]:016x} ({self.state[i]})")

        for i in self.intermediate_state:
            print(f"  intermediate_state[{i}] = 0x{self.intermediate_state[i]:016x} ({self.intermediate_state[i]})")

    def next_uint64(self):
        result = self.generate()
        return result

    def next_uint32(self):
        value64 = self.next_uint64()
        return (value64 >> 32) & 0xffffffff

    def generate(self):
        self.r1 = self.s1 * 5 & 0xffffffffffffffff
        self.r2 = self._rotl(self.r1, 7)
        self.n1 = self.r2 * 9 & 0xffffffffffffffff
        self.n2 = self.s1 << 17 & 0xffffffffffffffff
        self.n3 = self.s2 ^ self.s0
        self.n4 = self.s3 ^ self.s1
        self.n5 = self.s1 ^ self.n3
        self.n6 = self.s0 ^ self.n4
        self.n7 = self.n3 ^ self.n2
        self.n8 = self._rotl(self.n4, 45)

        self.s0 = self.n6
        self.s1 = self.n5
        self.s2 = self.n7
        self.s3 = self.n8
        return self.n1

    @staticmethod
    def _rotl(value, offset):
        x1 = (value << offset) & 0xffffffffffffffff
        x2 = value >> (64 - offset)
        return  x1 | x2

    @staticmethod
    def _rotr(value, offset):
        x1 = (value >> offset) & 0xffffffffffffffff
        x2 = value << (64 - offset)
        return x2 | x1


def test_generator():
    expected_values = [
        24777985201200000,
        3297275972100000,
        2101580424900000,
        17006381825400000,
        21254012722800000,
        28130643872100000,
        30511412820900000,
        20615290096500000,
        11348650655100000,
        8786896955100000
    ]
    
    xoshiro256 = Xoshiro256(10804161907448682703, 11460624974815451986, 15774960471522575440, 15521138194195770664)
    
    for i in range(10):
        generated = xoshiro256.next_uint32() * 9900000
        expected = expected_values[i]
        passed = generated == expected
        if not passed:
            return False

    return True


if __name__ == '__main__':
    # checked dotnet xoshiro256:
    # state=[]
    # next value from this stat=
    if not test_generator():
        print("Generator test failed")



