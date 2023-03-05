# Handles loading of packages into trucks
# 3 trucks, 2 drivers
from routing_graph import RoutingGraph
from csv_parser import RoutingProgramCSVParser
import pdb


class PackageManager:
    def __init__(self, packages):
        self.packages = packages

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
PACKAGE_9_ADDRESS = '410 S State St'


DISTANCE_TABLE_PATH = 'assets/distance_table.csv'
PACKAGE_TABLE_PATH = 'assets/package_file.csv'
packages = RoutingProgramCSVParser(PACKAGE_TABLE_PATH).parse()
addresses, matrix = RoutingProgramCSVParser(DISTANCE_TABLE_PATH).parse()
pm = PackageManager(packages)
pm.check_packages(RoutingGraph(matrix, addresses))
