import sys
import os

SYMBOLS = {
    'SP': 0, 'LCL': 1, 'ARG': 2, 'THIS': 3, 'THAT': 4,
    'R0': 0, 'R1': 1, 'R2': 2, 'R3': 3, 'R4': 4, 'R5': 5, 'R6': 6, 'R7': 7,
    'R8': 8, 'R9': 9, 'R10': 10, 'R11': 11, 'R12': 12, 'R13': 13, 'R14': 14, 'R15': 15,
    'SCREEN': 16384, 'KBD': 24576
}

COMP_TABLE = {
    "0": "0101010", "1": "0111111", "-1": "0111010", "D": "0001100",
    "A": "0110000", "!D": "0001101", "!A": "0011101", "-D": "0001111",
    "-A": "0011111", "D+1": "0011111", "A+1": "0011101", "D-1": "0001110",
    "A-1": "0110010", "D+A": "0000010", "D-A": "0010011", "A-D": "0000111",
    "D&A": "0000000", "D|A": "0010101",
    "M": "1110000", "!M": "1011101", "-M": "1011111", "M+1": "1011101",
    "M-1": "1110010", "D+M": "1000010", "D-M": "1010011", "M-D": "1000111",
    "D&M": "1000000", "D|M": "1010101"
}

DEST_TABLE = {
    "": "000", "M": "001", "D": "010", "MD": "011",
    "A": "100", "AM": "101", "AD": "110", "AMD": "111"
}

JUMP_TABLE = {
    "": "000", "JGT": "001", "JEQ": "010", "JGE": "011",
    "JLT": "100", "JNE": "101", "JLE": "110", "JMP": "111"
}

def clean_line(line):
    line = line.split("//")[0].strip()
    return line

def assemble(filename):
    with open(filename, "r") as f:
        raw_lines = f.readlines()

    symbol_table = dict(SYMBOLS)
    instructions = []
    rom_addr = 0

    # First pass: Build symbol table for labels
    for line_no, raw in enumerate(raw_lines, start=1):
        line = clean_line(raw)
        if not line:
            continue
        if line.startswith("(") and line.endswith(")"):
            label = line[1:-1]
            symbol_table[label] = rom_addr
        else:
            instructions.append((line_no, line))
            rom_addr += 1

    # Second pass: Process instructions & dynamic variables
    next_ram = 16
    output_lines = []
    
    for line_no, inst in instructions:
        if inst.startswith("@"):
            val = inst[1:]
            if val.isdigit():
                addr = int(val)
            else:
                if val not in symbol_table:
                    symbol_table[val] = next_ram
                    next_ram += 1
                addr = symbol_table[val]
            output_lines.append(format(addr, "016b"))
        else:
            dest, comp, jump = "", inst, ""
            if "=" in comp:
                dest, comp = comp.split("=", 1)
            if ";" in comp:
                comp, jump = comp.split(";", 1)
                
            dest = dest.strip()
            comp = comp.strip()
            jump = jump.strip()
            
            binary = "111" + COMP_TABLE[comp] + DEST_TABLE[dest] + JUMP_TABLE[jump]
            output_lines.append(binary)

    # Extra Feature for K=60 (60 mod 3 = 0): Save symbols.txt
    symbols_file = os.path.join(os.path.dirname(filename), "symbols.txt")
    with open(symbols_file, "w") as sf:
        for sym, addr in sorted(symbol_table.items(), key=lambda item: item[1]):
            sf.write(f"{sym}: {addr}\n")

    out_filename = filename.rsplit(".", 1)[0] + ".hack"
    with open(out_filename, "w") as out_f:
        out_f.write("\n".join(output_lines) + "\n")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        assemble(sys.argv[1])
    else:
        print("Usage: python assembler.py <file.asm>")