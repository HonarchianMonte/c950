class CreateHashMap:
    def __init__(self, initial_capacity=20):
        self.list = []
        for i in range(initial_capacity):
            self.list.append([])

    def insert(self, key, item):
        bucket = hash(key) % len(self.list)
        bucket_list = self.list[bucket]

        for kv in bucket_list:
            if kv[0] == key:
                kv[1] = item
                return True

        key_value = [key, item]
        bucket_list.append(key_value)
        return True

    def lookup(self, key):
        bucket = hash(key) % len(self.list)
        bucket_list = self.list[bucket]
        for pair in bucket_list:
            if key == pair[0]:
                return pair[1]
        return None

    def hash_remove(self, key):
        slot = hash(key) % len(self.list)
        destination = self.list[slot]
        if key in destination:
            destination.remove(key)
