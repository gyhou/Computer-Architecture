"""CPU functionality."""

import sys

# opcodes
LDI = 0b10000010
PRN = 0b01000111
HLT = 0b00000001
MUL = 0b10100010
PUSH = 0b01000101
POP = 0b01000110


class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.reg = [0] * 8
        self.reg[7] = 0xF4
        self.sp = self.reg[-1]
        self.pc = 0
        self.ram = [0] * 256
        self.fl = True
        self.branchtable = {}
        self.branchtable[LDI] = self.ldi
        self.branchtable[MUL] = self.mul
        self.branchtable[PRN] = self.prn
        self.branchtable[HLT] = self.hlt
        self.branchtable[PUSH] = self.push
        self.branchtable[POP] = self.pop

    def ldi(self, op_a, op_b):
        # Set the value of a register to an integer
        self.reg[op_a] = op_b
        print(f'LDI - Set reg[{op_a}] to {op_b}')
        self.pc += 3

    def mul(self, op_a, op_b):
        # Multiply the values in two registers together
        # and store the result in registerA
        # self.alu('MUL', operand_a, operand_b)
        print(
            f'MUL - Set reg[{op_a}] to {self.reg[op_a]}*{self.reg[op_b]}')
        self.reg[op_a] *= self.reg[op_b]
        self.pc += 3

    def prn(self, op_a, op_b):
        # Print value stored in the given register
        print(
            f'PRN - {self.reg[op_a]} is stored in reg[{op_a}]')
        self.pc += 2

    def hlt(self, op_a, op_b):
        # Flags can change based on the
        # operands given to the CMP opcode
        self.fl = False
        print("HLT - Exit the emulator")

    def push(self, op_a, op_b):
        # Push value in the given register to stack
        val = self.reg[op_a]
        print(f'Push {val} in reg[{op_a}] to {self.sp}')
        # Decrement SP
        self.sp -= 1
        # Copy value in registers to address by SP
        self.ram[self.sp] = val
        self.pc += 2

    def pop(self, op_a, op_b):
        # Pop value from top of stack to register
        # Copy value from address by SP to register
        val = self.ram[self.sp]
        print(f'Pop {val} from {self.sp} to reg[{op_a}]')
        self.reg[op_a] = val
        # Increment SP
        self.sp += 1
        self.pc += 2

    def load(self, filename):
        """Load a program into memory."""
        try:
            address = 0
            with open(filename) as f:
                print(f"Opening file: {filename}")
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
            print(f'{sys.argv[0]}: {filename} not found')
            sys.exit(2)

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        elif op == "MUL":
            print(
                f'MUL - Set register[{reg_a}] to {self.reg[reg_a]}*{self.reg[reg_b]}')
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
            self.fl,
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
        count = 1
        while self.fl:
            # Instruction Register - current instruction
            ir = self.ram[self.pc]
            print(f'Step {count}:')
            operand_a = self.ram_read(self.pc + 1)
            operand_b = self.ram_read(self.pc + 2)
            try:
                self.branchtable[ir](operand_a, operand_b)
            except KeyError:
                print(f"Error: Unknown command: {ir}")
                sys.exit(1)
            count += 1

    def ram_read(self, mar):
        return self.ram[mar]

    def ram_write(self, address, mdr):
        self.ram[address] = mdr
