import types
import dis

INSTRUCTIONS = {
    "GET_ITER": b"D\x00",
    "FOR_ITER": b"]\n",
    "COMPARE_OP<": b"k\x00\x00\x00\x00\x00",
    "COMPARE_OP>": b"k\x04\x00\x00\x00\x00",
    "POP_JUMP_FORWARD_IF_FALSE": b"r\x02",
    "JUMP_BACKWARD": b"\x8c\x0b",
    "LOAD_CONST": b"d",
    "STORE_FAST": b"}",
    "LOAD_FAST": b"|"
}


def op_to_bytecode(opcode_array):
    bytecode = b""
    for opcode in opcode_array:
        if opcode in INSTRUCTIONS:
            bytecode += INSTRUCTIONS[opcode]
        else:
            bytecode += opcode
    return bytecode


co_code_start = b"d\x01}\x01d\x02}\x02"
co_code_end = b"|\x01|\x02f\x02S\x00"

code_min_max = [
    "LOAD_FAST", b"\x00",
    "GET_ITER",
    "FOR_ITER",
    "STORE_FAST", b"\x03",
    "LOAD_FAST", b"\x03",
    "LOAD_FAST", b"\x01",
    "COMPARE_OP<",
    "POP_JUMP_FORWARD_IF_FALSE",
    "LOAD_FAST", b"\x03",
    "STORE_FAST", b"\x01",
    "JUMP_BACKWARD",
    # max
    "LOAD_FAST", b"\x00",
    "GET_ITER",
    "FOR_ITER",
    "STORE_FAST", b"\x03",
    "LOAD_FAST", b"\x03",
    "LOAD_FAST", b"\x02",
    "COMPARE_OP>",
    "POP_JUMP_FORWARD_IF_FALSE",
    "LOAD_FAST", b"\x03",
    "STORE_FAST", b"\x02",
    "JUMP_BACKWARD",
]

code_min_max_bytecode = op_to_bytecode(code_min_max)
print([int(byte) for byte in code_min_max_bytecode])

call_max = b"e\x02e\x00\xa6\x01\x00\x00\xab\x01\x00\x00\x00\x00\x00\x00\x00\x00"
full_code = co_code_start + code_min_max_bytecode + co_code_end
# dis.dis(full_code)
# exec(full_code)

import types
from random import randint


class Riddler:
    max_int: int
    min_int: int
    co_code_start: bytes
    co_code_end: bytes
    num_list: list[int]

    def __init__(self) -> None:
        self.max_int = 1000
        self.min_int = -1000
        self.co_code_start = b"d\x01}\x01d\x02}\x02"
        self.co_code_end = b"|\x01|\x02f\x02S\x00"
        self.num_list = [randint(self.min_int, self.max_int) for _ in range(10)]

    def ask_riddle(self) -> str:
        return """ 'In arrays deep, where numbers sprawl,
        I lurk unseen, both short and tall.
        Seek me out, in ranks I stand,
        The lowest low, the highest grand.

        What am i?'
        """

    def check_answer(self, answer: bytes) -> bool:
        _answer_func: types.FunctionType = types.FunctionType(
            self._construct_answer(answer), {}
        )
        print("calling _answer_func=%d:%d" % _answer_func(self.num_list))
        return _answer_func(self.num_list) == (min(self.num_list), max(self.num_list))

    def _construct_answer(self, answer: bytes) -> types.CodeType:
        co_code: bytearray = bytearray(self.co_code_start)
        co_code.extend(answer)
        co_code.extend(self.co_code_end)

        code_obj: types.CodeType = types.CodeType(
            1,
            0,
            0,
            4,
            3,
            3,
            bytes(co_code),
            (None, self.max_int, self.min_int),
            (),
            ("num_list", "min", "max", "num"),
            __file__,
            "_answer_func",
            "_answer_func",
            1,
            b"",
            b"",
            (),
            (),
        )
        dis.dis(code_obj)
        return code_obj

riddler = Riddler()
riddler.check_answer(code_min_max_bytecode)