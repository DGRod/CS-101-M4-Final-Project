from main_memory import MainMemoryBus
from cache import Cache

# ////////// Central Processing Unit //////////
# Helper function to convert Register string to index
def register_index(register):
    return int(register.strip("R$"))

# ---- Memory Register ----
class Register:

    def __init__(self, num_of_registers, num_of_history_registers=10):
        # Define separate registers for data and execution history
        self.data_registers = [0 for x in range(0, num_of_registers)]
        self.history_registers = [0 for x in range(0, num_of_history_registers)]


# ---- Arithmetic Logic Unit ----
class ALU:

    def __init__(self, register):
        self.register = register
    
    # // Arithmetic Operations //
    # Add Registers
    def add(self, operands):
        register = self.register.data_registers
        rd = register_index(operands[0])
        rs = register_index(operands[1])
        rt = register_index(operands[2])

        register[rd] = register[rs] + register[rt]
        print("Register #"+ str(rd), register[rd])
        return register[rd]
    
    # Add Constant(Immediate) to Register
    def addi(self, operands):
        register = self.register.data_registers
        rd = register_index(operands[0])
        rs = register_index(operands[1])
        immd = register_index(operands[2])

        register[rd] = register[rs] + immd
        print("Register #"+ str(rd), register[rd])
        return register[rd]
    
    # Subtract Registers
    def sub(self, operands):
        register = self.register.data_registers
        rd = register_index(operands[0])
        rs = register_index(operands[1])
        rt = register_index(operands[2])

        register[rd] = register[rs] - register[rt]
        print("Register #"+ str(rd), register[rd])
        return register[rd]
    
    # // Logical Operations //

    # // Conditional Operations //
    # Branch on Equal
    def beq(self, operands, parent):
        self.parent = parent
        register = self.register.data_registers
        rs = register_index(operands[0])
        rt = register_index(operands[1])
        offset = register_index(operands[2])
        # If Rs == Rt then skip offset # of instructions
        if register[rs] == register[rt]:
            self.parent.counter += int(offset)
            print("Operands are equal. Skipping " + str(offset) + " instructions")
        else:
            print("Operands are not equal")
    
    # Branch on Not Equal
    def bne(self, operands, parent):
        self.parent = parent
        register = self.register.data_registers
        rs = register_index(operands[0])
        rt = register_index(operands[1])
        offset = register_index(operands[2])
        # If Rs != Rt then skip offset # of instructions
        if register[rs] != register[rt]:
            self.parent.counter += int(offset)
            print("Operands are not equal. Skipping " + str(offset) + " instructions")
        else:
            print("Operands are equal")


# ---- Control Unit ----
class CU:

    def __init__(self, parent, register, alu, memory_bus):
        self.parent = parent
        self.register = register
        self.alu = alu
        self.memory_bus = memory_bus
    
    def run(self, input):
        split_input = input.split(" ")
        opcode = split_input[0]
        operands = split_input[1].split(",")
        print("Performing " + opcode, "on " + str(operands))

        if opcode == "ADD":
            self.alu.add(operands)
        
        elif opcode == "SUB":
            self.alu.sub(operands)

        elif opcode == "ADDI":
            self.alu.addi(operands)

        elif opcode == "BEQ":
            self.alu.beq(operands, self.parent)

        elif opcode == "BNE":
            self.alu.bne(operands, self.parent)
        
        elif opcode == "LW":
            self.lw(operands)

        elif opcode == "SW":
            self.sw(operands)
        
        elif opcode == "J":
            self.jump(operands, self.parent)

    # // Data Transfer Operations //
    # Load Word
    def lw(self, operands):
        rt = register_index(operands[0])
        address = register_index(operands[1])

        self.register.data_registers[rt] = self.memory_bus.memory[address]
        print(self.register.data_registers[rt])

    # Store Word
    def sw(self, operands):
        rt = register_index(operands[0])
        address = register_index(operands[1])

        self.memory_bus.memory[address] = self.register.data_registers[rt]
        print(self.memory_bus.memory[address])

    # // Jump Operations //
    # Jump
    def jump(self, operands, parent):
        self.parent = parent
        target = register_index(operands[0]) - 1
        self.parent.counter = int(target)
        print("Jumped to Instruction #" + str(target + 1))


class CPU:

    def __init__(self, register_size, cache, memory_bus):
        # External Connections
        self.cache = cache
        self.memory_bus = memory_bus

        # Internal Components
        self.counter = 0
        self.register = Register(register_size)
        self.alu = ALU(self.register)
        self.cu = CU(self, self.register, self.alu, self.memory_bus)
    
    def execute(self, instructions):
        instructions = instructions.split("\n")
        instruction_dict = {str(instructions.index(instruction)):instruction for instruction in instructions}
        print(instructions, instruction_dict)
        print("Counter " + str(self.counter))
        while str(self.counter) in instruction_dict.keys():
            print("Cycle: " + str(self.counter))
            self.cu.run(instruction_dict[str(self.counter)])
            self.counter += 1

        








# ////////// Setup //////////

datafile = "C:/Users/DGRod/OneDrive/Desktop/Python Code/CS 101 M4 Project/Input Data/Codecademy-Computer-Architecture-Portfolio-Project-Files/data_input.txt"


memory_bus = MainMemoryBus()
memory_bus.download(datafile)

register = Register(32, 10)
register.data_registers[6] = 4
register.data_registers[4] = 5


cpu = CPU(32, None, memory_bus)

# cpu.execute("ADDI R3,R6,R4")
# cpu.execute("SW R1,00000111")




# ////////// Input Processor //////////

print('Welcome to CPU Simulator!')
print("Please enter commands using MIPS Assembly Language\n")
print("/// OBJECTIVE: ")

lines = []
while True:
    line = input("")
    if line == "HALT ;":
        print("Execution Terminated")
        break
    lines.append(line)

instructions = "\n".join(lines)

cpu.execute(instructions)



