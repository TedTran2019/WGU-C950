# preliminary loading is a O(n) time complexity with a large constant and O(n) space complexity
# manual loading is a O(n) time complexity with a large constant and O(n) space complexity
# get_truck_packages is O(1) time complexity and O(1) space complexity
# set_packages is O(n) time and o(1) space
# load truck is O(n) time due to using set_packages and simply O(1) space
# check_packages isn't used by the program-- it was made by me to see which package addresses were invalid

from routing_graph import RoutingGraph
from csv_parser import RoutingProgramCSVParser

PACKAGE_9_ADDRESS = '410 S State St'


# Handles loading of packages into trucks
# 3 trucks, 2 drivers
class PackageManager:
    def __init__(self, packages):
        self.packages = packages
        self.truck_1_packages = []
        self.truck_2_packages = []
        self.truck_3_packages = []
        self.preliminary_loading()
        self.manual_loading()

    # This checks if every package address has a match in the target address list
    # Errors in packages 25/26: 5383 South 900 East #104
    # Changed vertex 26 match packages 25/26, changing "S" to "South"
    def check_packages(self, routing_graph):
        for package in self.packages:
            if routing_graph.lookup(package.address) == None:
                print(
                    f'Package {package.package_id} has an invalid address: {package.address}')

    # Package 9 address is incorrect and can't be corrected until 10:20
    # Packages 6, 25, 28, 32 are delayed until 9:05
    # Packages 3, 18, 36, 38 can only be on truck 2
    # Package 13, 14, 15, 16, 19, 20 must be delivered together
    # Package 1, 6, 13, 14, 16, 20, 25, 29, 30, 31, 34, 37, 40 must be delivered by 10:30 AM
    # Package 15 must be delivered by 9:00 AM
    # Packages start out ordered by package ID
    # 2/33, 4/40, 5/37/38, 7/29, 8/9/30, 13/39, 15/16/34, 20/21, 25/26, 27/35, 31/32
    # None of the truck 2's have deadlines
    # All of the "together" packages have deadlines
    # Ideally, these packages should always be together (same address = bundle together)
    # [0, 20, 21, 21, 21, 26, 24, 24, 22, 10, 23, 3, 13, 14, 15, 15, 18, 18, 5, 11, 9, 9, 2, 2, 25, 19, 19, 19, 8, 12, 12, 12, 6, 6, 1, 1, 7, 16, 4, 17, 17, 0]
    # Is the optimal path for 40 packages if there were no requirements
    def preliminary_loading(self):
        remaining_packages = []
        for package in self.packages:
            if package.package_id == 9:
                # Can still be loaded onto truck before 10:20, just can't be delivered until then
                package.delayed_until = '10:20'
                package.address = PACKAGE_9_ADDRESS
                self.truck_2_packages.append(package)
            elif package.package_id in [6, 25, 28, 32]:
                package.delayed_until = '9:05'
                self.truck_3_packages.append(package)
            elif package.package_id in [3, 18, 36, 38]:
                self.truck_2_packages.append(package)
            elif package.package_id in [13, 14, 15, 16, 19, 20]:
                self.truck_1_packages.append(package)
            else:
                remaining_packages.append(package)
        self.packages = remaining_packages

    # I put all the related addresses together (besides 37 and 30, because it has a deadline on truck 2 (slow truck))
    # I send off the trucks in this order: truck 1 (8 am), truck 3 (9:05 am), truck 2 (whenever a truck returns to hub)
    # truck 1 consists of: [13, 14, 15, 16, 19, 20, 21, 34, 39, 1, 2, 4, 7, 29, 33, 40] (16 packages)
    # truck 2 consists of: [9, 3, 18, 36, 38, 5, 8, 10, 11, 12, 17, 22, 23, 24] (14 packages)
    # truck 3 consists of: [6, 25, 28, 32, 26, 31, 27, 35, 37, 30] (10 packages)
    def manual_loading(self):
        remaining_packages = []
        for package in self.packages:
            if package.package_id in [21, 34, 39, 1, 2, 4, 7, 29, 33, 40]:
                self.truck_1_packages.append(package)
            elif package.package_id in [5, 8, 10, 11, 12, 17, 22, 23, 24]:
                self.truck_2_packages.append(package)
            elif package.package_id in [26, 31, 27, 35, 37, 30]:
                self.truck_3_packages.append(package)
            else:
                remaining_packages.append(package)
        self.packages = remaining_packages
        if remaining_packages:
            raise Exception(
                f'Not all packages were loaded, {len(remaining_packages)} remaining')

    def load_truck(self, truck, time):
        truck.packages = self.get_truck_packages(truck)
        self.set_packages(truck, time)

    def get_truck_packages(self, truck):
        if truck.truck_id == 1:
            return self.truck_1_packages
        elif truck.truck_id == 2:
            return self.truck_2_packages
        elif truck.truck_id == 3:
            return self.truck_3_packages
        else:
            raise Exception('Invalid truck ID')

    def set_packages(self, truck, time):
        for package in truck.packages:
            package.delivery_truck = truck.truck_id
            package.loaded_at = time
