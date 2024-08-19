import csv

class HashTable:
    def __init__(self, size=40):
        """Initialize the hash table with a specific size."""
        self.size = size
        self.table = [[] for _ in range(size)]

    def _hash(self, key):
        """Hash function to calculate the index for a given key."""
        return key % self.size
    
    def insert(self, key, address, deadline, city, zip_code, weight, status):
        """Insert a key-value pair into the hash table."""
        index = self._hash(key)
        bucket = self.table[index]

        for i, kv in enumerate(bucket):
            k, v = kv
            if key == k:
                bucket[i] = (key, {"address": address, "deadline": deadline, "city": city, "zip_code": zip_code, "weight": weight, "status": status})
                return
            
        # If key not found, append the new key-value pair
        bucket.append((key, {"address": address, "deadline": deadline, "city": city, "zip_code": zip_code, "weight": weight, "status": status}))

    def lookup(self, key):
        """Lookup a value by its key in the hash table."""
        index = self._hash(key)
        bucket = self.table[index]

        for k, v in bucket:
            if key == k:
                return v #Return the value if found
            
        return None #Return None if key not found
    
    def load_from_csv(self, csv_file):
        """Load data from a CSV file and insert it into the hash table."""
        with open(csv_file, mode='r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                self.insert(
                    int(row['Package ID']), 
                    row['Address'], 
                    row['Delivery Deadline'], 
                    row['City'], 
                    row['Zip'], 
                    float(row['Weight KILO']), 
                    "At hub"  # You can change this default status as needed
                )

# Example Usage
if __name__ == "__main__":
    # Create a hash table instance
    ht = HashTable()

    # Load package data from the CSV
    ht.load_from_csv('./data/package_data.csv')

    # Lookup and print a package
    package = ht.lookup(1)
    print(f"Package 1 details: {package}")

    package = ht.lookup(2)
    print(f"Package 2 details: {package}")

    package = ht.lookup(4) 
    print(f"Package 4 details: {package}") 
