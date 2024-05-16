

class Register:

    def __init__(self, name, num_of_registers, num_of_history_registers=10):
        self.name = name
        self.data_registers = [0 for x in range(0, num_of_registers)]
        self.history_registers = [0 for x in range(0, num_of_history_registers)]


class MemoryBus:
    
    

class ALU:

    def __init__(self, name, register):
        self.name = name
        self.register = register
    
    def run(self, input):
        split_input = input.split(" ")
        opcode = split_input[0]
        operands = split_input[1].split(",")
        print(opcode, operands)

        if opcode == "ADD":
            self.add(operands)
        
        elif opcode == "SUB":
            self.sub(operands)

        elif opcode == "ADDI":
            self.addi(operands)
        
    def add(self, operands):
        register = self.register.data_registers
        rd = int(operands[0].strip("R$"))
        rs = int(operands[1].strip("R$"))
        rt = int(operands[2].strip("R$"))

        register[rd] = register[rs] + register[rt]
        print("Register #"+ str(rd), register[rd])
        return register[rd]
    
    def addi(self, operands):
        register = self.register.data_registers
        rd = int(operands[0].strip("R$"))
        rs = int(operands[1].strip("R$"))
        immd = int(operands[2].strip("R$"))

        register[rd] = register[rs] + immd
        print("Register #"+ str(rd), register[rd])
        return register[rd]
    
    def sub(self, operands):
        register = self.register.data_registers
        rd = int(operands[0].strip("R$"))
        rs = int(operands[1].strip("R$"))
        rt = int(operands[2].strip("R$"))

        register[rd] = register[rs] - register[rt]
        print("Register #"+ str(rd), register[rd])
        return register[rd]


register1 = Register("register1", 22)
register1.data_registers[6] = 4
register1.data_registers[4] = 5

alu1 = ALU("alu1", register1)

alu1.run("ADDI R3,R6,R4")