from main_memory import MainMemoryBus
from random import randint
from datetime import datetime

# ////////// Cache ///////////
class Cache:
    def __init__(self, main_memory, num_of_registers, number_of_sets=0, replacement_policy=None, write_policy=None):
        self.main_memory = main_memory
        self.number_of_sets = number_of_sets
        self.replacement_policy = replacement_policy
        self.write_policy = write_policy

        self.cache_active = False
        self.counter = 0
        
        self.cache = [{"set":None, "address":None, "data":None, "last use":None} for x in range(0,num_of_registers)]
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
            block["last use"] = None
        print("Cache Flushed")
        #print(self.cache)

    def replace(self, address, data=None):
        # If no data is provided, set data equal to the value stored at the provided address in MainMemoryBus
        if data == None:
            data = self.main_memory.memory[address]
        
        # Check if Cache has room for a new block
        for block in self.cache:
            if block["address"] == None:
                # Empty block detected, fill with data from MainMemoryBus
                block["address"] = address
                block["data"] = data
                block["last use"] = datetime.datetime.now()
                print(block["last use"])
                return block
        # Cache full, choose which block to replace
        index_to_replace = self.execute_policy()       
        block = self.cache[index_to_replace]
        # Check if Write-Back Policy is enabled
        if self.write_policy == "BACK":
            # Write data to MainMemoryBus
            self.main_memory.memory[block["address"]] = block["data"]
        # Overwrite block data    
        block["address"] = address
        block["data"] = data
        block["last use"] = datetime.datetime.now()
        return block

    def search(self, target):
        for block in self.cache:
            if block["address"] == target:
                # Cache Hit -- Return data stored in Cache
                print("Cache Hit")
                block["last use"] = datetime.datetime.now()
                print(block["last use"])
                return block["data"]
            else:
                # Cache Miss -- Access MainMemoryBus
                print("Cache Miss")
                block = self.replace(target)
                return block["data"]
    
    def set_replacement_policy(self, new_policy):
        if new_policy.upper() == "RANDOM" or new_policy.upper() == "DISABLE":
            self.replacement_policy = None
        elif new_policy.upper() == "FIFO":
            self.replacement_policy = "FIFO"
        elif new_policy.upper() == "LRU":
            self.replacement_policy = "LRU"
        else:
            print("Not a valid Replacement Policy")

    def set_write_policy(self, new_policy):
        if new_policy.upper() == "THROUGH" or new_policy.upper() == "DISABLE":
            self.write_policy = None
        elif new_policy.upper() == "BACK":
            self.write_policy = "BACK"
        else:
            print("Not a valid Write Policy")   

    def execute_policy(self):
        if self.replacement_policy == None:
            # No Replacement Policy selected, choose a random index to overwrite
            index_to_replace = randint(0,len(self.cache) - 1)

        elif self.replacement_policy == "FIFO":
            # First In First Out (FIFO) Replacement Policy selected, choose the oldest index to overwrite
            index_to_replace = self.counter
            # Update the counter
            if self.counter < self.num_of_registers - 1:
                self.counter += 1
            else:
                self.counter = 0
        
        elif self.replacement_policy == "LRU":
            # Least Recently Used (LRU) Replacement Policy selected, choose the least recently used index to overwrite
            lru_index = 0
            for index in range(0, len(self.cache)):
                block = self.cache[index]
                if block["last use"] < self.cache[lru_index]["last use"]:
                    lru_index = index
            index_to_replace = lru_index

        return index_to_replace
    
    def write(self, address, data):
        if self.write_policy == None:
            # Default Write-Through Policy selected, write data to Cache and MainMemoryBus simultaneously
            self.replace(address, data)
            self.main_memory.memory[address] = data

        elif self.write_policy == "BACK":
            # Write-Back Policy selected, write data to Cache now and write data to MainMemoryBus when the data is about to be replaced
            self.replace(address, data)











main_memory = MainMemoryBus()
test = Cache(main_memory, 32)

# for item in test.cache:
#     print(item)