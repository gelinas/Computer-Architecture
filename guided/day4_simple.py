import sys

PRINT_BEEJ     = 1
HALT           = 2
PRINT_NUM      = 3
SAVE           = 4  # Save a value to a register
PRINT_REGISTER = 5  # Print a value from a register
ADD            = 6  # regA += regB
PUSH           = 7
POP            = 8
CALL           = 9
RET            = 10

memory = [0] * 32

register = [0] * 8

pc = 0
running = True

SP = 7

def load_memory(filename):
    address = 0
    try:
        with open(filename) as f:
            for line in f:

                # Ignore comments
                comment_split = line.split("#")

                # Strip out whitespace
                num = comment_split[0].strip()

                # Ignore blank lines
                if num == '':
                    continue

                val = int(num)
                memory[address] = val
                address += 1

    except FileNotFoundError:
        print("File not found")
        sys.exit(2)


if len(sys.argv) != 2:
    print("usage: simple.py filename")
    sys.exit(1)

filename = sys.argv[1]
load_memory(filename)


while running:
    command = memory[pc]
    # print(memory)
    # print(register)
    # print("-----")
    print(pc)

    if command == PRINT_BEEJ:
        print("Beej!")
        pc += 1

    elif command == HALT:
        running = False
        pc += 1

    elif command == PRINT_NUM:
        num = memory[pc + 1]
        print(num)
        pc += 2

    elif command == SAVE:
        num = memory[pc + 1]
        reg = memory[pc + 2]
        register[reg] = num
        pc += 3

    elif command == PRINT_REGISTER:
        reg = memory[pc + 1]
        print(register[reg])
        pc += 2

    elif command == ADD:
        reg_a = memory[pc + 1]
        reg_b = memory[pc + 2]
        register[reg_a] += register[reg_b]
        pc += 3

    elif command == PUSH:
        reg = memory[pc + 1]
        val = register[reg]
        # Decrement the SP.
        register[SP] = (register[SP] - 1) % (len(memory))
        # Copy the value in the given register to the address pointed to by SP.
        memory[register[SP]] = val
        pc += 2

    elif command == POP:
        reg = memory[pc + 1]
        val = memory[register[SP]]
        # Copy the value from the address pointed to by SP to the given register.
        register[reg] = val
        # Increment SP.
        register[SP] += 1
        pc += 2

    elif command == CALL:
        # The address of the instruction directly after CALL is pushed onto the stack.
        # This allows us to return to where we left off when the subroutine finishes executing.
        register[SP] -= 1
        memory[register[SP]] = pc + 2

        # The PC is set to the address stored in the given register.
        # We jump to that location in RAM and execute the first instruction in the subroutine.
        # The PC can move forward or backwards from its current location.
        reg = memory[pc + 1]
        pc = register[reg]

    elif command == RET:
        # Return from subroutine.
        # Pop the value from the top of the stack and store it in the PC.
        pc = memory[register[SP]]
        register[SP] += 1

    else:
        print(f"Unknown instruction: {command}")
        sys.exit(1)