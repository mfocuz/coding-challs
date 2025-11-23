import re
import sys


class VMTranslatorParser:
    TYPES = {
        "push": "C_PUSH",
        "pop": "C_POP",
        "add": "C_ARITHMETIC",
        "sub": "C_ARITHMETIC",
        "neg": "C_ARITHMETIC",
        "eq": "C_ARITHMETIC",
        "gt": "C_ARITHMETIC",
        "lt": "C_ARITHMETIC",
        "and": "C_ARITHMETIC",
        "or": "C_ARITHMETIC",
        "not": "C_ARITHMETIC",
    }

    current_line = 0
    current_instruction = ""

    def __init__(self, input_file):
        try:
            self.file = open(input_file, 'r')
            lines_raw = self.file.readlines()

            self.lines = []
            for line in lines_raw:
                if not line.startswith("//") and len(line.strip()) != 0:
                    self.lines.append(line.strip())

        except IOError as error:
            print(f"Error opening *.vm file for parsing: {error}")

    def stop(self):
        self.file.close()

    def has_more_lines(self):
        if self.current_line < len(self.lines):
            self.advance()
            return True
        else:
            return False

    def advance(self):
        self.current_instruction = self.lines[self.current_line]
        self.current_line += 1

    def command_type(self):
        command = self._parse_command()

        if command is not None:
            return self.TYPES[command]
        else:
            return "C_INVALID"

    def command(self):
        return self._parse_command()

    def arg1(self):
        pattern = r'\w+\s*(\w+).*'
        match = re.search(pattern, self.current_instruction)

        if match:
            return match.group(1)
        else:
            return None

    def arg2(self):
        pattern = r'\w+\s*\w+\s*(\d*)'
        match = re.search(pattern, self.current_instruction)

        if match:
            return match.group(1)
        else:
            return None

    def _parse_command(self):
        pattern = r'(\w+).*'
        match = re.search(pattern, self.current_instruction)

        if match.group(1) and match.group(1) in self.TYPES:
            return match.group(1)
        else:
            return None


# VM Memory Segments
# 0 - Stack
# 1 - LCL
# 2 - ARG
# 3 - THIS
# 4 - THAT
# 5-12 - temp segment
# 13-15 - general purpose
# 16-255 - static
# 256+ - stack
class VMTranslatorWriter:
    SEGMENTS = {
        "constant": "SP",
        "local": "LCL",
        "argument": "ARG",
        "this": "THIS",
        "that": "THAT",
        "temp": "R5",
        "pointer": "R15",
        "static": "R16",
    }

    # continue from here, need to impletemt eq, gt, lt
    C_ARITHMETIC_2_OPERAND = {
        "add": "M=D+M\n",
        "sub": "M=D-M\n",
        "eq": "",
        "gt": "",
        "lt": "",
        "and": "M=D&M\n",
        "or": "M=D|M\n",
        "not": "M=!M\n",
    }

    C_ARITHMETIC_1_OPERAND = {
        "neg": "M=-M\n",
    }

    def __init__(self, output_file):
        try:
            self.file = open(output_file, 'w')
        except IOError as error:
            raise error

    def stop(self):
        try:
            self.file.close()
        except IOError as error:
            print(f"Error closing: {error}")

    def write_arithmetic(self, command):
        if command in self.C_ARITHMETIC_2_OPERAND:
            asm = self.two_operands(command)
        elif command in self.C_ARITHMETIC_1_OPERAND:
            asm = self.one_operand(command)
        else:
            raise Exception("invalid command")

        self.file.write(asm)

    def one_operand(self, command):
        asm = ""

        asm += self.sp_minus()
        asm += "@SP\n"
        asm += "A=M\n"
        asm += self.C_ARITHMETIC_1_OPERAND[command]

        return asm

    # pushes result onto the stack
    def two_operands(self, command):
        asm = ""

        # pop last 2 values from stack
        asm += self.sp_minus()
        asm += "@SP\n"
        asm += "A=M\n"
        asm += "D=M\n"
        asm += "A=A-1\n"
        asm += self.C_ARITHMETIC_2_OPERAND[command]

        return asm

    def write_push_pop(self, command_type, segment, index):
        asm = ""
        segment = self.SEGMENTS[segment]

        # push and pop are commands about stack only, we do not push/pop on other segments
        # we consider values are there somehow
        if command_type == "C_PUSH":
            # for constant, we need to push exact value on stack
            if segment == "constant":
                self.push_constant(index)
            else:
                asm = self.push(segment, index)
        elif command_type == "C_POP":
            asm = self.pop(segment, index)

        self.file.write(asm)

    def push_constant(self, constant):
        asm = ""

        # set D to value need to push
        asm += f"@{constant}\n"
        asm += "D=A\n"

        # push value on stack
        asm += "@SP\n"
        asm += "A=M\n"
        asm += "M=D\n"
        asm += "@SP\n"
        asm += self.sp_plus()

    def push(self, segment, index):
        asm = ""

        asm += self.get_segment_address_into_D(segment, index)

        # push value D into stack
        asm += "@SP\n"
        asm += "A=M\n"
        asm += "M=D\n"
        asm += self.sp_plus()

        return asm

    def pop(self, segment, index):
        asm = ""

        asm += self.get_segment_address_into_D(segment, index)

        # save address of segment on stack as temp value, do not increment stack
        asm += "@SP\n"
        asm += "A=M\n"
        asm += "M=D\n"

        # pop value from stack into D
        asm += self.sp_minus()
        asm += "A=M\n"
        asm += "D=M\n"

        # A points to stack, go to next memory address, and jump into it's value(which is segment address)
        asm += "A=M+1"
        asm += "A=M"

        # Assign popped value to segment address
        asm += "M=D"

        return asm

    @staticmethod
    def sp_plus():
        return "@SP\n" + "M=M+1\n"

    @staticmethod
    def sp_minus():
        return "@SP\n" + "M=M-1\n"

    @staticmethod
    def get_segment_address_into_D(segment, index):
        asm = ""
        asm += f"@{segment}\n"
        asm += "D=M\n"
        asm += f"@{index}\n"
        asm += "D=D+A\n"
        return asm


if __name__ == "__main__":
    parser = None
    writer = None

    try:
        parser = VMTranslatorParser(sys.argv[1])
        writer = VMTranslatorWriter(sys.argv[2])
    except IOError as error:
        print(f"Error opening: {error}")

    while parser.has_more_lines():
        command_type = parser.command_type()
        if command_type == "C_PUSH" or command_type == "C_POP":
            writer.write_push_pop(command_type, parser.arg1(), parser.arg2())
        elif command_type == "C_ARITHMETIC":
            writer.write_arithmetic(parser.command())
        else:
            print("Invalid command type")

    parser.stop()
    writer.stop()

