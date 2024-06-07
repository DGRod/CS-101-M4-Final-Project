from main_memory import MainMemoryBus
from random import randint

# ////////// Cache ///////////
class Cache:
    def __init__(self, main_memory, num_of_registers, number_of_sets=0):
        self.main_memory = main_memory
        
        self.cache = [{"set":None, "address":None, "data":None} for x in range(0,num_of_registers)]

        print(self.cache)
    
    def replace(self, address, replacement_policy=None):

        # Check if Cache is full
        for block in self.cache:
            if block["address"] == None:
                block["address"] = address
                block["data"] = self.main_memory.memory[address]
                return block
        # If Cache is full, choose which block to replace       
        if replacement_policy == "FIFO":
            pass
        # If no Replacement Policy is selected, replace a random block
        else:
            block = self.cache[randint(0,len(self.cache) - 1)]
            block["address"] = address
            block["data"] = self.main_memory.memory[address]
            return block


    def search(self, target):
        for block in self.cache:
            if block["address"] == target:
                # Return data stored in Cache
                print("Cache Hit")
                return block["data"]
            else:
                print("Cache Miss")
                # Access MainMemoryBus
                block = self.replace(target)
                return block["data"]










main_memory = MainMemoryBus()
test = Cache(main_memory, 32)

# for item in test.cache:
#     print(item)