class CreateHashMap:
    def __init__(self, initial_capacity=20):
        # Initialize the hash table with a capacity of 20
        self.list = []
        for i in range(initial_capacity):
            self.list.append([]) # Each bucket is an empty list to store items

    def insert(self, key, item):
        # Figure out which slot the item should go into
        bucket = hash(key) % len(self.list)
        bucket_list = self.list[bucket]

        #Check if the key is already in the slot
        for kv in bucket_list:
            if kv[0] == key:
                kv[1] = item 
                return True

        # If the key isn't there, add the new item to the slot
        key_value = [key, item]
        bucket_list.append(key_value)
        return True

    def lookup(self, key):
        #Figure out which slot the key would be in
        bucket = hash(key) % len(self.list)
        bucket_list = self.list[bucket]

        # Search for the key in that slot and return the item if found
        for pair in bucket_list:
            if key == pair[0]:
                return pair[1]
        return None 

    def hash_remove(self, key):
        slot = hash(key) % len(self.list)
        destination = self.list[slot]
        if key in destination:
            destination.remove(key)
            return True  # Indicate that the removal was successful or that the key wasn't found
        return False 