# ////////// Main Memory Bus //////////
class MainMemoryBus:
    
    def __init__(self):
        self.memory = {int(bin(x).split("b")[-1]):0 for x in range(0, 256)}
    
    def download(self, datafile):
        # Load in a file with MainMemory initial conditions
        with open(datafile, 'r') as data:
            lines = data.readlines()
            for line in lines:
                split_line = line.split(",")
                address = int(split_line[0])
                value = int(split_line[1])
                self.memory[address] = value
            #print(self.memory)

