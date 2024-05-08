from Crypto.Util.number import getPrime, isPrime, long_to_bytes

e = 65537
N = 1
while (N - 1) % e == 0:
    N = getPrime(2048)

def xor(a, b):
    return bytes(x^y for x,y in zip(a,b))

class MySeededHash():
    def __init__(self, N, e):
        self.N = N
        self.e = e
        self._state = b"\x00" * 256
        self.seen = set()

    def _hash_block(self, block):
        assert len(block) == 256

        if block in self.seen:
            raise ValueError("This looks too familiar... :o")
        self.seen.add(block)

        data = int.from_bytes(block, "big")
        if data < 2 or data >= N-1:
            raise ValueError("Please ensure data is supported by hash function :|")

        data = pow(data, self.e, self.N)
        if data in self.seen:
            raise ValueError("Collisions are cheating!!! >:(")
        self.seen.add(data)

        return data.to_bytes(256, "big")

    def update(self, data):
        assert len(data) % 256 == 0

        for block in range(0, len(data), 256):
            block = data[block:block+256]
            self._state = xor(self._state, self._hash_block(block))

        return self

    def hexdigest(self):
        return self._state.hex()

    def __repr__(self):
        return f"MySeededHash({self.N}, {self.e})"


def egcd(a, b):
    if a == 0:
        return (b, 0, 1)
    else:
        g, y, x = egcd(b % a, a)
        return (g, x - (b // a) * y, y)


def modinv(a, m):
    g, x, y = egcd(a, m)
    if g != 1:
        raise Exception('modular inverse does not exist')
    else:
        return x % m


def solution(e, N):
    d = modinv(e, N-1)

    block_1 = pow(0xf0, d, N)
    block_2 = pow(0x0f, d, N)
    block_3 = pow(0xff, d, N)
    return block_1.to_bytes(256, "big") + block_2.to_bytes(256, "big") + block_3.to_bytes(256, "big")


def main():
    hash = MySeededHash(N, e)
    print(hash)

    print("Give me your string that hashes to 0...")
    preimage = solution(e, N)
    print("Solution block=%s" % preimage.hex())
    if len(preimage) < 256 or len(preimage) % 256 != 0:
        raise ValueError("Invalid input!")

    zero = hash.update(preimage).hexdigest()
    print("hash(input) ==", zero)
    if zero == "00" * 256:
        print("Task Solved!")
    else:
        print("...")

main()
