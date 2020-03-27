"""CPU functionality."""

import sys

HLT  = 1    # 0b00000001
RET  = 17   # 0b00010001
PRN  = 71   # 0b01000111
PUSH = 69   # 0b01000101
POP  = 70   # 0b01000110
CALL = 80   # 0b01010000
JMP  = 84   # 0b01010100
JEQ  = 85   # 0b01010101
JNE  = 86   # 0b01010110
LDI  = 130  # 0b10000010 
ADD  = 160  # 0b10100000
MUL  = 162  # 0b10100010
CMP  = 167  # 0b10100111

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        # 256 bytes of RAM
        self.ram = [0] * 256
        # 8 bytes of register
        self.reg = [0] * 8
        # program counter
        self.pc = 0
        # stack pointer register address (default to 7)
        self.sp = 7
        # stack pointer initialiaed to high memory address from RAM
        self.reg[self.sp] = 255
        # instruction register for address of currently executing subroutine
        self.ir = 0
        # flag for 00000LGE for less, greater, equal comparisons
        self.flag = 0b00000000

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

    def alu(self, op, reg_a, reg_b=0):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        elif op == "MUL":
            self.reg[reg_a] *= self.reg[reg_b]
        elif op == "CMP":
            if self.reg[reg_a] < self.reg[reg_b]:
                self.flag = 0b00000100
            elif self.reg[reg_a] < self.reg[reg_b]:
                self.flag = 0b00000010
            elif self.reg[reg_a] == self.reg[reg_b]:
                self.flag = 0b00000001
        elif op == "AND":
            self.reg[reg_a] = self.reg[reg_a] & self.reg[reg_b]
        elif op == "OR":
            self.reg[reg_a] = self.reg[reg_a] | self.reg[reg_b]
        elif op == "XOR":
            self.reg[reg_a] = self.reg[reg_a] ^ self.reg[reg_b]
        elif op == "NOT":
            self.reg[reg_a] = ~self.reg[reg_a]
        elif op == "SHL":
            self.reg[reg_a] = self.reg[reg_a] << self.reg[reg_b]
        elif op == "SHR":
            self.reg[reg_a] = self.reg[reg_a] >> self.reg[reg_b]

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
                # load a piece of data in to the register
                # register address in self.pc + 1
                # data to load in register in self.pc + 2
                reg_addr = self.ram[self.pc + 1] 
                data = self.ram[self.pc + 2]
                # print(f"data loaded {data:>08b}")
                self.reg[reg_addr] = data
                self.pc += 3

            elif command == PRN:
                # print argument stored in register
                # register address at self.pc + 1
                reg_addr = self.ram[self.pc + 1] 
                print(self.reg[reg_addr])
                self.pc += 2

            elif command == CMP:
                # compares operands a and b stored in the register
                # register addresses for operand a in self.pc + 1 
                # register address for operand b in self.pc + 2
                # return result to flag
                # implement with ALU
                op_a_addr = self.ram[self.pc + 1]
                op_b_addr = self.ram[self.pc + 2]
                self.alu("CMP", op_a_addr, op_b_addr)
                # print(f"comparison result: {self.flag:>0b}")
                self.pc += 3

            elif command == ADD:
                # adds operands a and b stored in the register
                # register addresses for operand a in self.pc + 1 
                # register address for operand b in self.pc + 2
                # return result to R0
                # implement with ALU
                op_a_addr = self.ram[self.pc + 1]
                op_b_addr = self.ram[self.pc + 2]
                self.alu("ADD", op_a_addr, op_b_addr)
                self.pc += 3

            elif command == MUL:
                # multiply operands a and b stored in the register
                # register addresses for operand a in self.pc + 1 
                # register address for operand b in self.pc + 2
                # return result to R0
                # implement with ALU
                op_a_addr = self.ram[self.pc + 1]
                op_b_addr = self.ram[self.pc + 2]
                self.alu("MUL", op_a_addr, op_b_addr)
                self.pc += 3
                # implement with direct code
                # op_a_addr = self.ram[self.pc + 1]
                # op_b_addr = self.ram[self.pc + 2]
                # op_a = self.reg[op_a_addr]
                # op_b = self.reg[op_b_addr]
                # result = op_a * op_b
                # self.reg[0] = result
                # self.pc += 3

            elif command == PUSH:
                # moves an item from the register address at pc + 1 into the stack
                # decrements the memory address stored in the stack pointer
                reg_addr = self.ram[self.pc + 1]
                # get value to place in stack from register address at pc + 1
                value = self.reg[reg_addr]
                # decrement the memory address stored in the stack pointer
                self.reg[self.sp] -= 1
                # copy the value onto the stack in memory
                self.ram[self.reg[self.sp]] = value
                self.pc += 2

            elif command == POP:
                # move an item off the stack and into the register address at pc + 1
                # increments the memory address stored in the stack pointer
                reg_addr = self.ram[self.pc + 1]
                # get value to place in register from stack
                value = self.ram[self.reg[self.sp]]
                # copy the value to the register address
                self.reg[reg_addr] = value
                # increment the memory address stored in the stack pointer
                self.reg[self.sp] += 1
                self.pc += 2

            elif command == CALL:
                # The address of the instruction directly after CALL is pushed onto the stack.
                # the place to return is at pc + 2
                # This allows us to return to where we left off when the subroutine finishes executing.
                self.reg[self.sp] -= 1
                self.ram[self.reg[self.sp]] = self.pc + 2
                # The PC is set to the address stored in the given register.
                # We jump to that location in RAM and execute the first instruction in the subroutine.
                # The PC can move forward or backwards from its current location.
                self.pc = self.reg[self.ram[self.pc + 1]]

            elif command == RET:
                # Return from subroutine.
                # Pop the value from the top of the stack and store it in the PC.
                self.pc = self.ram[self.reg[self.sp]]
                self.reg[self.sp] += 1

            elif command == JMP:
                # If `equal` flag is set (true), jump to the address stored in the given register.
                self.pc = self.reg[self.ram[self.pc + 1]]

            elif command == JEQ:
                # if equal flag true, jump to the address stored in the given register.
                if self.flag & 0b00000001 is 1:
                    self.pc = self.reg[self.ram[self.pc + 1]]
                else:
                    self.pc += 2

            elif command == JNE:
                # if equal flag false, jump to the address stored in the given register.
                if self.flag & 0b00000001 is 0:
                    self.pc = self.reg[self.ram[self.pc + 1]]
                else:
                    self.pc += 2

            else:
                print(f"Unknown instruction: {command:>08b}")
                sys.exit(1)  