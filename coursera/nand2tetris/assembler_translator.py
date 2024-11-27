import os.path
import re
import sys


COMP_OPERATIONS = {
    "0":    [0,1,0,1,0,1,0],
    "1":    [0,1,1,1,1,1,1],
    "-1":   [0,1,1,1,0,1,0],
    "D":    [0,0,0,1,1,0,0],
    "A":    [0,1,1,0,0,0,0],
    "!D":   [0,0,0,1,1,0,1],
    "!A":   [0,1,1,0,0,0,1],
    "-D":   [0,0,0,1,1,1,1],
    "-A":   [0,1,1,0,0,1,1],
    "D+1":  [0,0,1,1,1,1,1],
    "A+1":  [0,1,1,0,1,1,1],
    "D-1":  [0,0,0,1,1,1,0],
    "A-1":  [0,1,1,0,0,1,0],
    "D+A":  [0,0,0,0,0,1,0],
    "D-A":  [0,0,1,0,0,1,1],
    "A-D":  [0,0,0,0,1,1,1],
    "D&A":  [0,0,0,0,0,0,0],
    "D|A":  [0,0,1,0,1,0,1],
    "M":    [1,1,1,0,0,0,0],
    "!M":   [1,1,1,0,0,0,1],
    "-M":   [1,1,1,0,0,1,1],
    "M+1":  [1,1,1,0,1,1,1],
    "M-1":  [1,1,1,0,0,1,0],
    "D+M":  [1,0,0,0,0,1,0],
    "D-M":  [1,0,1,0,0,1,1],
    "M-D":  [1,0,0,0,1,1,1],
    "D&M":  [1,0,0,0,0,0,0],
    "D|M":  [1,0,1,0,1,0,1]
}

DEST_OPERATIONS = {
    None:   [0,0,0],
    "M":    [0,0,1],
    "D":    [0,1,0],
    "DM":   [0,1,1],
    "A":    [1,0,0],
    "AM":   [1,0,1],
    "AD":   [1,1,0],
    "ADM":  [1,1,1],
}

JMP_OPERATIONS = {
    None:   [0,0,0],
    "JGT":  [0,0,1],
    "JEQ":  [0,1,0],
    "JGE":  [0,1,1],
    "JLT":  [1,0,0],
    "JNE":  [1,0,1],
    "JLE":  [1,1,0],
    "JMP":  [1,1,1],
}

class SymbolTable:
    symbol_table = {}
    n = 16

    def __init__(self):
        self.symbol_table = {}
        for i in range(0, 16):
            self.symbol_table[f"R{i}"] = i

        self.symbol_table["SCREEN"] = 16384
        self.symbol_table["KBD"] = 24576
        n = 16

    def add_symbol(self, symbol, address):
        if address is None:
            self.symbol_table[symbol] = self.n
            self.n += 1
        else:
            self.symbol_table[symbol] = address

    def get_address(self, symbol):
        return self.symbol_table[symbol]

    def defined(self, symbol):
        if symbol in self.symbol_table:
            return True
        else:
            return False


def first_pass(symbol_table, assembler_code):
    pattern_lable = r'\(([A-Z0-9]*)\)'
    instr_pointer = 0
    for i, line in enumerate(assembler_code):
        if line.startswith("("):
            match = re.match(pattern_lable, line)
            if match and not symbol_table.defined(match.group(1)):
                symbol_table.add_symbol(match.group(1), instr_pointer)

            assembler_code[i] = None

        instr_pointer += 1

    return  symbol_table


def second_pass(symbol_table, assembler_code):
    pattern_address = r'@([A-Z0-9]*)'
    pattern_instruction = r'([MDA])=([MDA01+\-&|!]{0,3});?(J..)?'
    pattern_instr_no_dest = r'([MDA01]{1});?(J..)?'
    binary_code = ""

    for instruction in assembler_code:
        if instruction is None:
            continue

        # @ADDR case
        if instruction.startswith("@"):
            match = re.match(pattern_address, instruction)
            if match and not symbol_table.defined(match.group(1)):
                symbol_table.add_symbol(match.group(1), None)

            binary_code += bin(symbol_table.get_address(match.group(1)))[2:].zfill(16) + "\n"

        # instr with destination case
        elif re.match(pattern_instruction, instruction):
            match = re.match(pattern_instruction, instruction)

            dest = match.group(1)
            comp = match.group(2)
            jmp = match.group(3) or None

            operation = [1, 1, 1] + COMP_OPERATIONS[comp] + DEST_OPERATIONS[dest] + JMP_OPERATIONS[jmp]
            binary_code += "".join(map(str, operation)) + "\n"

        # instr with no destination case
        elif re.match(pattern_instr_no_dest, instruction):
            match = re.match(pattern_instr_no_dest, instruction)

            comp = match.group(1)
            jmp = match.group(2)

            operation = [1, 1, 1] + COMP_OPERATIONS[comp] + [0,0,0] + JMP_OPERATIONS[jmp]
            binary_code += "".join(map(str, operation)) + "\n"

        else:
            print("Compilation error!")
            sys.exit(1)


    return binary_code


def translate_to_assembly(assembler_code):
    # Initialization
    symbol_table = SymbolTable()
    # 1st Pass
    symbol_table = first_pass(symbol_table, assembler_code)
    # 2nd Pass
    binary_code = second_pass(symbol_table, assembler_code)

    return binary_code


def read_file_content_and_clear(file):
    try:
        clean = []
        with open(file, "r") as f:
            lines = f.read().split("\n")
            for line in lines:
                clean_line = re.sub(r'//.*', '',line).replace(" ", "")
                if clean_line != "":
                    clean.append(clean_line)

            return clean

    except FileNotFoundError:
        print(f"File {file} not found.")


def write_to_file(file, content):
    try:
        with open(file, "w") as f:
            f.write(content)
    except Exception as e:
        print(f"An error occurred: {e}")


def compare_files(test, result):
    try:
        with open(test, "r") as test_file, open(result, "r") as result_file:
            while True:
                chunk1 = test_file.readline()
                chunk2 = result_file.readline()

                if chunk1 != chunk2:
                    return False

                if not chunk1:
                    break

        return True
    except Exception as e:
        print(f"An error occurred during comparison: {e}")


if __name__ == "__main__":
    PROJECT_DIR = "/home/mfocuz/WorkEnv/learn/nand2tetris/nand2tetris/projects/06/pong/"
    assembler_file = "Pong"

    assembler_code = read_file_content_and_clear(os.path.join(PROJECT_DIR, assembler_file + ".asm"))
    binary_code = translate_to_assembly(assembler_code)
    write_to_file(os.path.join(PROJECT_DIR, assembler_file + ".result"), binary_code)
    if compare_files(os.path.join(PROJECT_DIR, "origin." + assembler_file + ".hack"), os.path.join(PROJECT_DIR, assembler_file + ".result")):
        print("Compilation OK!")



