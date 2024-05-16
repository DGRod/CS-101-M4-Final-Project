

# ////////// Main Memory Bus //////////

class MainMemoryBus:
    
    def __init__(self):
        self.memory = {int(bin(x).split("b")[-1]):0 for x in range(0, 256)}
    
    def download(self, datafile):
        with open(datafile, 'r') as data:
            lines = data.readlines()
            for line in lines:
                split_line = line.split(",")
                address = int(split_line[0])
                value = int(split_line[1])
                self.memory[address] = value
            print(self.memory)


# ////////// Cache //////////


# ////////// Central Processing Unit //////////
# ---- Memory Register ----
class Register:

    def __init__(self, num_of_registers, num_of_history_registers=10):
        self.data_registers = [0 for x in range(0, num_of_registers)]
        self.history_registers = [0 for x in range(0, num_of_history_registers)]


# ---- Arithmetic Logic Unit ----
class ALU:

    def __init__(self, register):
        self.register = register
        
    # Add Registers
    def add(self, operands):
        register = self.register.data_registers
        rd = int(operands[0].strip("R$"))
        rs = int(operands[1].strip("R$"))
        rt = int(operands[2].strip("R$"))

        register[rd] = register[rs] + register[rt]
        print("Register #"+ str(rd), register[rd])
        return register[rd]
    
    # Add Constant(Immediate) to Register
    def addi(self, operands):
        register = self.register.data_registers
        rd = int(operands[0].strip("R$"))
        rs = int(operands[1].strip("R$"))
        immd = int(operands[2].strip("R$"))

        register[rd] = register[rs] + immd
        print("Register #"+ str(rd), register[rd])
        return register[rd]
    
    # Subtract Registers
    def sub(self, operands):
        register = self.register.data_registers
        rd = int(operands[0].strip("R$"))
        rs = int(operands[1].strip("R$"))
        rt = int(operands[2].strip("R$"))

        register[rd] = register[rs] - register[rt]
        print("Register #"+ str(rd), register[rd])
        return register[rd]


# ---- Control Unit ----
class CU:

    def __init__(self, register, alu, memory_bus):
        self.register = register
        self.alu = alu
        self.memory_bus = memory_bus
    
    def run(self, input):
        split_input = input.split(" ")
        opcode = split_input[0]
        operands = split_input[1].split(",")
        print(opcode, operands)

        if opcode == "ADD":
            self.alu.add(operands)
        
        elif opcode == "SUB":
            self.alu.sub(operands)

        elif opcode == "ADDI":
            self.alu.addi(operands)
        
        elif opcode == "LW":
            self.lw(operands)

        elif opcode == "SW":
            self.sw(operands)

    # Load Word
    def lw(self, operands):
        rt = int(operands[0].strip("R$"))
        address = int(operands[1].strip("R$"))

        self.register.data_registers[rt] = self.memory_bus.memory[address]

    # Store Word
    def sw(self, operands):
        rt = int(operands[0].strip("R$"))
        address = int(operands[1].strip("R$"))

        self.memory_bus.memory[address] = self.register.data_registers[rt]
        print(self.memory_bus.memory[address])


class CPU:

    def __init__(self, cu, alu, register, cache, memory_bus):
        # Internal Components
        self.cu = cu
        self.alu = alu
        self.register = register

        # External Connections
        self.cache = cache
        self.memory_bus = memory_bus




# ////////// Input Processor //////////








datafile = "C:/Users/DGRod/OneDrive/Desktop/Python Code/CS 101 M4 Project/Input Data/Codecademy-Computer-Architecture-Portfolio-Project-Files/data_input.txt"


memory_bus = MainMemoryBus()
memory_bus.download(datafile)

register = Register(22, 10)
register.data_registers[6] = 4
register.data_registers[4] = 5

alu = ALU(register)
cu = CU(register, alu, memory_bus)

cpu = CPU(cu, alu, register, None, memory_bus)

cu.run("ADDI R3,R6,R4")
cu.run("SW R1,00000111")
