
class Xoshiro256Base:
    @staticmethod
    def _rotl(value, offset):
        x1 = (value << offset) & 0xffffffffffffffff
        x2 = value >> (64 - offset)
        return  x1 | x2

    @staticmethod
    def _rotr(value, offset):
        x1 = (value >> offset) & 0xffffffffffffffff
        x2 = (value << (64 - offset)) & 0xffffffffffffffff
        return x2 | x1

class Xoshiro256State:
    BIT64 = 0xffffffffffffffff
    def __init__(self, s0, s1, s2, s3):
        self.s0 = s0 & self.BIT64
        self.s1 = s1 & self.BIT64
        self.s2 = s2 & self.BIT64
        self.s3 = s3 & self.BIT64
        self.r1 = self.r2 = 0
        self.n1 = self.n2 = self.n3 = self.n4 = self.n5 = self.n6 = self.n7 = self.n8 = 0

class Xoshiro256(Xoshiro256Base):
    current_state = 0
    prng_states = []

    def __init__(self, s0, s1, s2, s3):
        self.current_state = 0
        self.prng_states = []
        state = Xoshiro256State(s0, s1, s2, s3)
        self.prng_states.append(state)

    def next_state(self):
        self.current_state += 1

    def next_uint64(self):
        result = self.generate()
        return result
    def next_uint60(self):
        return self.next_uint64() >> 4

    def next_uint32(self):
        value64 = self.next_uint64()
        return (value64 >> 32) & 0xffffffff

    def generate(self):
        current_state = self.prng_states[self.current_state]
        current_state.r1 = current_state.s1 * 5 & 0xffffffffffffffff
        current_state.r2 = self._rotl(current_state.r1, 7)
        current_state.n1 = current_state.r2 * 9 & 0xffffffffffffffff

        current_state.n2 = current_state.s1 << 17 & 0xffffffffffffffff
        current_state.n3 = current_state.s2 ^ current_state.s0
        current_state.n4 = current_state.s3 ^ current_state.s1
        current_state.n5 = current_state.s1 ^ current_state.n3
        current_state.n6 = current_state.s0 ^ current_state.n4
        current_state.n7 = current_state.n3 ^ current_state.n2
        current_state.n8 = self._rotl(current_state.n4, 45)

        self.prng_states[self.current_state] = current_state
        self.next_state()
        new_state = Xoshiro256State(current_state.n6, current_state.n5, current_state.n7, current_state.n8)
        self.prng_states.append(new_state)

        return current_state.n1


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
        generated = xoshiro256.next_uint32()
        expected = expected_values[i]
        print(f"Value {i+1}: Generated: {generated}, multiplied: {generated * 9900000}, Expected: {expected}")
        passed = generated * 9900000 == expected
        if not passed:
            return False

    return True


if __name__ == '__main__':
    if not test_generator():
        print("Generator test failed")
    else:
        print("Generator test passed")

    xoshiro256 = Xoshiro256(10804161907448682703, 11460624974815451986, 15774960471522575440, 15521138194195770664)
    for i in range(20):
        value = xoshiro256.generate()
        print("64bit: %s, 32bit:%s" % (value, value >> 32))








