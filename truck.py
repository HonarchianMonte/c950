class Truck:
    def __init__(self, capacity, speed, packages, mileage, address, depart_time):
        self.capacity = capacity
        self.speed = speed
        self.packages = packages
        self.mileage = mileage
        self.address = address
        self.depart_time = depart_time
        self.time = depart_time

    def __str__(self):
        return f"Truck {self.capacity}: {len(self.packages)} packages, mileage {self.mileage:.1f}, currently at {self.address}, departed at {self.depart_time}"