"""CPU functionality."""

import sys

# import os
# os.getcwd()
# os.path.exists(examples)


class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256

        self.reg = [0] * 8

        self.pc = 0

        self.ir = 0

        self.fl = 6

        self.op_table = {
            0b10000010: self.ldi,
            0b01000111: self.prn,
            0b10100010: self.mult,
            0b00000001: self.hlt,
            0b01010110: self.jne,
            0b01010100: self.jmp,
            0b01010101: self.jeq,
            0b10100111: self.cmp
        }

    def ram_read(self, address):
        return self.ram[address]

    def ram_write(self, value, address):
        self.ram[address] = value

    def ldi(self, op1, op2):
        self.reg[op1] = op2

    def mult(self, op1, op2):
        self.reg[op1] = self.reg[op1] * self.reg[op2]

    def hlt(self, op1, op2):
        sys.exit()

    def prn(self, op1, op2):
        print(self.reg[op1])

    def cmp(self, op1, op2):
        num1 = self.reg[op1]
        num2 = self.reg[op2]

        if num1 == num2:
            self.reg[self.fl] = 1
        elif num1 > num2:
            self.reg[self.fl] = 2
        else:
            self.reg[self.fl] = 4

    def jmp(self, op1, op2):
        self.pc = self.reg[op1]
        return True

    def jeq(self, op1, op2):
        if self.reg[self.fl] == 1:
            return self.jmp(op1, 0)

    def jne(self, op1, op2):
        num = self.reg[self.fl]
        if num == 2 or num == 4:
            return self.jmp(op1, 0)

    def load(self):
        """Load a program into memory."""

        address = 0

        # For now, we've just hardcoded a program:

        # program = [
        #     # From print8.ls8
        #     0b10000010,  # LDI R0,8
        #     0b00000000,
        #     0b00001000,
        #     0b01000111,  # PRN R0
        #     0b00000000,
        #     0b00000001,  # HLT
        # ]

        file = open('sctest.ls8',  "r")
        for line in file.readlines():
            try:
                x = line[:line.index("#")]
            except ValueError:
                x = line

            try:
                y = int(x, 2)
                self.ram[address] = y
            except ValueError:
                continue
            address += 1

        # for instruction in program:
        #     self.ram[address] = instruction
        #     address += 1

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        # elif op == "SUB": etc
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
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

        # print(self.ram_read(2))

        # print(self.reg[2])

        # self.trace()

        while True:
            self.ir = self.ram[self.pc]
            op1 = self.ram[self.pc + 1]
            op2 = self.ram[self.pc + 2]

            noJumper = self.op_table[self.ir](op1, op2)

            if not noJumper:
                self.pc += (self.ir >> 6) + 1
