

class Register:

    def __init__(self, name):
        self.name = name
        self.data_registers = [0, 0, 0, 4, 0, 0, 8, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        self.history_registers = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

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
            result_register = operands[0]
            sum = 0
            for operand in operands:
                sum += self.register.data_registers[int(operand.strip("R"))]
            print(sum)
            return sum



register1 = Register("register1")


alu1 = ALU("alu1", register1)

alu1.run("ADD R3,R6")