"""CPU functionality."""

import sys

HLT = 1
LDI = 130
PRN = 71

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256
        self.reg = [0] * 8
        self.pc = 0

    def load(self, filepath):
        """Load a program into memory."""
        program = []
        address = 0
        try:
            with open(filepath, 'r') as f:
                for line in f:
                    # Ignore comments
                    comment_split = line.split("#")
                    # Strip out whitespace
                    num = comment_split[0].strip()
                    # Ignore blank lines
                    if num == '':
                        continue
                    program.append('0b' + num)
                    # print(program)
            for instruction in program:
                self.ram[address] = eval(instruction)
                address += 1

        except FileNotFoundError:
            print("File not found")
            sys.exit(2)

        # # For now, we've just hardcoded a program:
        # address = 0
        # program = [
        #     # From print8.ls8
        #     0b10000010, # LDI R0,8
        #     0b00000000,
        #     0b00001000,
        #     0b01000111, # PRN R0
        #     0b00000000,
        #     0b00000001, # HLT
        # ]
        # for instruction in program:
        #     self.ram[address] = instruction
        #     address += 1


    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        #elif op == "SUB": etc
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            #self.fl,
            #self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def ram_read(self, address):
        """
        read a byte from RAM
        """
        return self.ram[address]

    def ram_write(self, address, byte):
        """
        write a byte to RAM
        """
        self.ram[address] = byte

    def run(self):
        """Run the CPU."""
        running = True
        self.pc = 0
        while running:
            command = self.ram[self.pc]

            if command == HLT:
                running = False
                self.pc += 1

            elif command == LDI:
                reg_addr = self.ram[self.pc + 1] 
                data = self.ram[self.pc + 2]
                self.reg[reg_addr] = data
                self.pc += 3

            elif command == PRN:
                reg_addr = self.ram[self.pc + 1] 
                print(self.reg[reg_addr])
                self.pc += 2

            else:
                print(f"Unknown instruction: {command}")
                sys.exit(1)