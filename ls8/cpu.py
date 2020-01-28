"""CPU functionality."""

import sys

# opcode values
LDI = 0b10000010
PRN = 0b01000111
HLT = 0b00000001
MUL = 0b10100010


class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.reg = [0] * 8
        self.pc = 0
        self.ram = [0] * 256

    def load(self, filename):
        """Load a program into memory."""
        try:
            address = 0
            with open(filename) as f:
                for line in f:
                    # Remove comments
                    comment_split = line.split('#')
                    num = comment_split[0].strip()
                    # Skip blank lines
                    if num == '':
                        continue
                    # Base 10, but ls-8 is base 2
                    value = int(num, 2)
                    self.ram_write(address, value)
                    address += 1

        except FileNotFoundError:
            print(f'{sys.argv[0]}: {sys.argv[1]} not found')
            sys.exit(2)

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        elif op == "MUL":
            print(
                f'Set register[{reg_a}] to {self.reg[reg_a]}*{self.reg[reg_b]}')
            self.reg[reg_a] *= self.reg[reg_b]
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. 
        You might want to call this from run() 
        if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            # self.fl,
            # self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def run(self):
        """Run the CPU."""
        # Flags can change based on the
        # operands given to the CMP opcode
        FL = True

        while FL:
            # Instruction Register - current instruction
            ir = self.ram[self.pc]
            operand_a = self.ram_read(self.pc + 1)
            operand_b = self.ram_read(self.pc + 2)

            if ir == LDI:
                self.reg[operand_a] = operand_b
                print(f'Set register[{operand_a}] to {operand_b}')
                self.pc += 3
            elif ir == MUL:
                self.alu('MUL', operand_a, operand_b)
                self.pc += 3
            elif ir == PRN:
                print(
                    f'{self.reg[operand_a]} is stored in register[{operand_a}]')
                self.pc += 2
            elif ir == HLT:
                print("Exit the emulator")
                FL = False
            else:
                print(f"Error: Unknown command: {ir}")
                sys.exit(1)

    def ram_read(self, mar):
        return self.ram[mar]

    def ram_write(self, address, mdr):
        self.ram[address] = mdr
