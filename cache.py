from main_memory import MainMemoryBus
from random import randint

# ////////// Cache ///////////
class Cache:
    def __init__(self, main_memory, num_of_registers, number_of_sets=0):
        self.main_memory = main_memory

        self.cache_active = False

        self.counter = 0
        
        self.cache = [{"set":None, "address":None, "data":None} for x in range(0,num_of_registers)]
        #print(self.cache)

    def status(self, code):
        # Set Cache status to OFF
        if code == '0':
            self.cache_active = False
        # Set Cache status to ON
        elif code == '1':
            self.cache_active = True
        # Flush Cache
        elif code == '2':
            self.flush()
        print("Cache Active: " + str(self.cache_active))

    def flush(self):
        for block in self.cache:
            block["address"] = None
            block["data"] = None
        print("Cache Flushed")
        #print(self.cache)

    def replace(self, address, replacement_policy=None):

        # Check if Cache is full
        for block in self.cache:
            if block["address"] == None:
                # Empty block detected, fill with data from MainMemoryBus
                block["address"] = address
                block["data"] = self.main_memory.memory[address]
                return block
        # Cache full, choose which block to replace       
        if replacement_policy == "FIFO":
            block = self.cache[self.counter]
            block["address"] = address
            block["data"] = self.main_memory.memory[address]

            if self.counter < self.num_of_registers - 1:
                self.counter += 1
            else:
                self.counter = 0
            return block
        # If no Replacement Policy is selected, replace a random block
        else:
            block = self.cache[randint(0,len(self.cache) - 1)]
            block["address"] = address
            block["data"] = self.main_memory.memory[address]
            return block


    def search(self, target):
        for block in self.cache:
            if block["address"] == target:
                # Cache Hit -- Return data stored in Cache
                print("Cache Hit")
                return block["data"]
            else:
                # Cache Miss -- Access MainMemoryBus
                print("Cache Miss")
                block = self.replace(target)
                return block["data"]










main_memory = MainMemoryBus()
test = Cache(main_memory, 32)

# for item in test.cache:
#     print(item)