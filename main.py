# Monte Honarchian
# Student ID: 011467947

import csv
import datetime
from truck import Truck
from hashTable import CreateHashMap
from package import Package

# Load CSV files
with open("DATA/distances.csv") as csvfile:
    CSV_Distance = list(csv.reader(csvfile))

with open("DATA/addresses.csv") as csvfile1:
    CSV_Address = list(csv.reader(csvfile1))

with open("DATA/packages.csv") as csvfile2:
    CSV_Package = list(csv.reader(csvfile2))

# Create hash table
package_hash_table = CreateHashMap()

# Load packages into hash table
def load_package_data(filename, package_hash_table):
    with open(filename) as package_info:
        package_data = csv.reader(package_info)
        for package in package_data:
            pID = int(package[0])
            pAddress = package[1]
            pCity = package[2]
            pState = package[3]
            pZipcode = package[4]
            pDeadline_time = package[5]
            pWeight = package[6]
            pNotes = package[7]
            pStatus = "At Hub"

            # Package object
            p = Package(pID, pAddress, pCity, pState, pZipcode, pDeadline_time, pWeight, pStatus, pNotes)
            package_hash_table.insert(pID, p)

# Method for finding distance between two addresses
def distance_in_between(x_value, y_value):
    distance = CSV_Distance[x_value][y_value]
    if distance == '':
        distance = CSV_Distance[y_value][x_value]
    return float(distance)

# Method to get address number from string
def extract_address(address):
    for row in CSV_Address:
        if address in row[2]:
            return int(row[0])

# Create truck objects
truck1 = Truck(16, 18, [13, 15, 16, 19, 1, 14, 20, 29, 30, 31, 34, 37, 40], 0.0, "4001 South 700 East", datetime.timedelta(hours=8))
truck2 = Truck(16, 18, [3, 12, 17, 18, 21, 22, 23, 24, 26, 27, 35, 36, 38, 39], 0.0, "4001 South 700 East", datetime.timedelta(hours=10, minutes=20))
truck3 = Truck(16, 18, [2, 4, 5, 6, 7, 8, 9, 10, 11, 25, 28, 32, 33], 0.0, "4001 South 700 East", datetime.timedelta(hours=9, minutes=32))

# Load packages into hash table
load_package_data("DATA/packages.csv", package_hash_table)

# Manually update package #9 to start with an incorrect address
p9 = Package(9, "Wrong Address", "Salt Lake City", "UT", "84101", "EOD", 2, "At Hub", "This package has an incorrect address and will be updated at 10:20 AM")
package_hash_table.insert(p9.ID, p9)

# Method for delivering packages using the nearest neighbor algorithm
def deliver_packages(truck_number, truck, package_hash_table):
    not_delivered = []
    for packageID in truck.packages:
        package = package_hash_table.lookup(packageID)
        not_delivered.append(package)
    truck.packages.clear()

    while len(not_delivered) > 0:
        next_address = 2000
        next_package = None
        for package in not_delivered:
            if package.ID == 9 and truck.time < datetime.timedelta(hours=10, minutes=20):
                # Skip package #9 until after 10:20 AM
                continue
            if distance_in_between(extract_address(truck.address), extract_address(package.address)) <= next_address:
                next_address = distance_in_between(extract_address(truck.address), extract_address(package.address))
                next_package = package
        if next_package:
            truck.packages.append(next_package.ID)
            not_delivered.remove(next_package)
            truck.mileage += next_address
            truck.address = next_package.address
            truck.time += datetime.timedelta(hours=next_address / 18)
            if truck.time >= truck.depart_time:
                next_package.delivery_time = truck.time
                next_package.departure_time = truck.depart_time
                next_package.status = "Delivered"
        else:
            break

    print(f"Truck #{truck_number}: {len(truck.packages)} packages, mileage {truck.mileage:.1f}, currently at {truck.address}, departed at {truck.depart_time} has completed its deliveries with {truck.mileage:.1f} miles driven.")

# Now include the step to update Package #9's address and insert it back into the hash table
def update_package_9():
    p9_updated = package_hash_table.lookup(9)
    p9_updated.address = "410 S State St"
    p9_updated.zipcode = "84111"
    package_hash_table.insert(p9_updated.ID, p9_updated)

# Reset Package #9 to the incorrect address if time is before 10:20 AM
def reset_package_9_if_needed(check_time):
    if check_time < datetime.timedelta(hours=10, minutes=20):
        p9_reset = package_hash_table.lookup(9)
        p9_reset.address = "Wrong Address"
        p9_reset.zipcode = "84101"
        package_hash_table.insert(p9_reset.ID, p9_reset)

def reset_truck(truck):
    truck.mileage = 0.0
    truck.address = "4001 South 700 East"  # Reset to the hub's address
    truck.time = truck.depart_time  # Reset to the initial departure time

def reset_all_trucks_and_packages():
    # Reset all trucks to initial state
    reset_truck(truck1)
    reset_truck(truck2)
    reset_truck(truck3)

    # Reload all package data to ensure no carryover from previous runs
    load_package_data("DATA/packages.csv", package_hash_table)

    # Manually reset package #9 to its incorrect address
    p9 = Package(9, "Wrong Address", "Salt Lake City", "UT", "84101", "EOD", 2, "At Hub", "This package has an incorrect address and will be updated at 10:20 AM")
    package_hash_table.insert(p9.ID, p9)

def start_simulation():
    # Reset everything before starting the simulation
    reset_all_trucks_and_packages()

    print("Starting Delivery Simulation...")

    deliver_packages(1, truck1, package_hash_table)
    deliver_packages(2, truck2, package_hash_table)
    truck3.depart_time = min(truck1.time, truck2.time)
    update_package_9()  # Update Package #9 after 10:20 AM
    deliver_packages(3, truck3, package_hash_table)

    total_mileage = truck1.mileage + truck2.mileage + truck3.mileage
    total_time = max(truck1.time, truck2.time, truck3.time) - datetime.timedelta(hours=8)
    print(f"Total mileage for all trucks: {total_mileage:.1f} miles")
    print(f"Total time for all trucks combined: {total_time}")

def convert_time(time_str):
    # Convert the input time string "HH:MM AM/PM" to a datetime.timedelta object
    time_obj = datetime.datetime.strptime(time_str, '%I:%M %p')
    return datetime.timedelta(hours=time_obj.hour, minutes=time_obj.minute)

def check_all_package_statuses():
    time_input = input("Enter the time to check status (HH:MM AM/PM): ")
    check_time = convert_time(time_input)

    # Reset Package #9 if the check time is before 10:20 AM
    reset_package_9_if_needed(check_time)

    print(f"\nChecking package status at {check_time}\n")

    # Display status for all packages on Truck 1
    print("Truck 1 Packages:")
    for packageID in truck1.packages:
        package = package_hash_table.lookup(packageID)
        package.update_status(check_time)
        print(f"Package ID: {package.ID}, Address: {package.address}, City: {package.city}, "
              f"Zipcode: {package.zipcode}, Deadline: {package.deadline}, "
              f"Weight: {package.weight}, Status: {package.status}, "
              f"Delivery Time: {package.delivery_time}")
        
    # Display status for all packages on Truck 2
    print("\nTruck 2 Packages:")
    for packageID in truck2.packages:
        package = package_hash_table.lookup(packageID)
        package.update_status(check_time)
        print(f"Package ID: {package.ID}, Address: {package.address}, City: {package.city}, "
              f"Zipcode: {package.zipcode}, Deadline: {package.deadline}, "
              f"Weight: {package.weight}, Status: {package.status}, "
              f"Delivery Time: {package.delivery_time}")

    # Display status for all packages on Truck 3
    print("\nTruck 3 Packages:")
    for packageID in truck3.packages:
        package = package_hash_table.lookup(packageID)
        package.update_status(check_time)
        print(f"Package ID: {package.ID}, Address: {package.address}, City: {package.city}, "
              f"Zipcode: {package.zipcode}, Deadline: {package.deadline}, "
              f"Weight: {package.weight}, Status: {package.status}, "
              f"Delivery Time: {package.delivery_time}")

#Individual Package Status
def check_individual_package_status():
    package_id = int(input("Enter the package ID to check status: "))
    time_input = input("Enter the time to check status (HH:MM AM/PM): ")
    check_time = convert_time(time_input)

    # Reset Package #9 if the check time is before 10:20 AM
    reset_package_9_if_needed(check_time)

    package = package_hash_table.lookup(package_id)
    package.update_status(check_time)

    print(f"Package ID: {package.ID}, Address: {package.address}, City: {package.city}, "
          f"Zipcode: {package.zipcode}, Deadline: {package.deadline}, "
          f"Weight: {package.weight}, Status: {package.status}, "
          f"Delivery Time: {package.delivery_time}")

def main_menu():
    while True:
        # Display the main menu options
        print("\nWGUPS Routing Program")
        print("1. Start Delivery Simulation")
        print("2. Check All Package Statuses")
        print("3. Check Individual Package Status")
        print("4. Exit")
        choice = input("> ")

        if choice == '1':
            start_simulation()
        elif choice == '2':
            check_all_package_statuses()
        elif choice == '3':
            check_individual_package_status()
        elif choice == '4':
            break
        else:
            print("Invalid choice, please try again.")

if __name__ == "__main__":
    main_menu()
