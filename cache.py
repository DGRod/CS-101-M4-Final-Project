from main_memory import MainMemoryBus
from random import randint
from datetime import datetime

# ////////// Cache ///////////
class Cache:
    def __init__(self, main_memory, num_of_registers, number_of_sets=1, replacement_policy=None, write_policy=None):
        self.main_memory = main_memory
        self.number_of_sets = number_of_sets
        self.replacement_policy = replacement_policy
        self.write_policy = write_policy

        self.cache_active = False
        self.counter = [{"set":x, "counter":0} for x in range(0,self.number_of_sets)]
        self.cache = [{"index":int(x), "set":0, "address":None, "data":None, "last use":None} for x in range(0,num_of_registers)]

        # Determine how many blocks in the Cache are associated with each set
        blocks_per_set = len(self.cache) // self.number_of_sets
        print(blocks_per_set)
        # Assign each block a set number
        for i in range(0,len(self.cache)):
            self.cache[i]["set"] = i // blocks_per_set
            print(self.cache[i])

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
        # Determine what subset of the Cache to consider, based on the Cache's Set Associativity
        subset = self.subset(address)
        # Check if the 'subset' has room for a new block
        for subset_block in subset:
            if subset_block["address"] == None:
                # Empty block detected, fill with data from MainMemoryBus
                block = self.cache[subset_block["index"]]
                block["address"] = address
                block["data"] = data
                block["last use"] = datetime.now()
                print(block["last use"])
                # print(subset)
                return block
        # Cache full, choose which block to replace
        index_to_replace = self.execute_policy(subset)
        block = self.cache[index_to_replace]
        print("index to replace", index_to_replace)
        print("block", block)
        # Check if Write-Back Policy is enabled
        if self.write_policy == "BACK":
            # Write data to MainMemoryBus
            print("saving data in MainMemoryBus . . .")
            self.main_memory.memory[block["address"]] = block["data"]
        # Overwrite block data    
        block["address"] = address
        block["data"] = data
        block["last use"] = datetime.now()
        return block

    def search(self, target):
        print("target", target)
        for block in self.cache:
            print(block["address"])
            if block["address"] == target:
                # Cache Hit -- Return data stored in Cache
                print("Cache Hit")
                block["last use"] = datetime.now()
                print(block["last use"])
                # print(self.cache)
                return block["data"]
            
        # Cache Miss -- Access MainMemoryBus
        print("Cache Miss")
        # print(self.cache)
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

    def execute_policy(self, subset):
        if self.replacement_policy == None:
            # No Replacement Policy selected, choose a random index to overwrite
            print("Random Replacement Policy selected")
            index_to_replace = randint(0,len(subset) - 1)

        elif self.replacement_policy == "FIFO":
            print("FIFO Replacement Policy selected")
            # First In First Out (FIFO) Replacement Policy selected, choose the oldest index to overwrite
            # Select the counter associated with this set from 'self.counter'
            set_number = int(subset[0]["set"])
            counter = self.counter[set_number]["counter"]
            index_to_replace = subset[counter]["index"]
            # Update the counter
            if counter < len(subset) - 1:
                self.counter[set_number]["counter"] += 1
            else:
                self.counter[set_number]["counter"] = 0
        
        elif self.replacement_policy == "LRU":
            print("LRU Replacement Policy selected")
            # Least Recently Used (LRU) Replacement Policy selected, choose the least recently used index to overwrite
            lru_index = subset[0]["index"]
            for subset_block in subset:
                block = self.cache[subset_block["index"]]
                if block["last use"] < self.cache[lru_index]["last use"]:
                    lru_index = subset_block["index"]
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

    def subset(self, address):
        subset = []
        # Determine how many addresses in the MainMemoryBus are associated with each set
        addresses_per_set = len(self.main_memory.memory) / self.number_of_sets
        # Convert the 'address' into an integer value
        int_address = int(str(address), 2)
        # Determine which set the 'address' belongs to
        address_set = int(int_address // addresses_per_set)
        # Set subset equal to a list of all blocks that belong to the selected set
        for block in self.cache:
            if block["set"] == address_set:
                subset.append(block)

        return subset







# main_memory = MainMemoryBus()
# test = Cache(main_memory, 32)

# test.subset(1111101)
# for item in test.cache:
#     print(item)