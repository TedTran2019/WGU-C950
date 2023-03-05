# Handles loading of packages into trucks
# 3 trucks, 2 drivers
from routing_graph import RoutingGraph
from csv_parser import RoutingProgramCSVParser

PACKAGE_9_ADDRESS = '410 S State St'


class PackageManager:
    def __init__(self, packages):
        self.packages = packages
        self.truck_1_packages = []
        self.truck_2_packages = []
        self.truck_3_packages = []
        # self.preliminary_loading()

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
    # Ideally, these packages should always be together (same address = bundle together)
    def preliminary_loading(self):
        remaining_packages = []
        for package in self.packages:
            if package.package_id in [3, 6, 9, 13, 14, 15, 16, 18, 19, 20, 25, 28, 32, 36, 38]:
                if package.package_id == 9:
                    package.delayed_until = '10:20'
                    package.address = PACKAGE_9_ADDRESS
                    self.truck_3_packages.append(package)
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

    def load_truck(self, truck):
        truck.packages = self.packages
