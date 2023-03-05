from csv_parser import RoutingProgramCSVParser
from truck import Truck
from routing_graph import RoutingGraph
from package_manager import PackageManager
import config

DISTANCE_TABLE_PATH = 'assets/distance_table.csv'
PACKAGE_FILE_PATH = 'assets/package_file.csv'


class WgupsRoutingProgram:
    def __init__(self):
        self.trucks = [Truck(1), Truck(2), Truck(3)]
        self.packages = RoutingProgramCSVParser(PACKAGE_FILE_PATH).parse()
        self.package_manager = PackageManager(self.packages)
        target_addresses, matrix = RoutingProgramCSVParser(
            DISTANCE_TABLE_PATH).parse()
        self.routing_graph = RoutingGraph(matrix, target_addresses)
        print('WGUPS Routing Program initialized')

    def run(self):
        # Testing with all packages before doing each truck individually
        addresses = [package.address for package in self.packages]
        all_orders = self.routing_graph.two_opt(addresses)
        # print(all_orders)
        # self.report()
        print(config.CURRENT_TIME)
        config.increment_global_time(5)
        print(config.CURRENT_TIME)
        # self.report()
        # self.deliver_packages(all_orders)

    def total_truck_mileage(self):
        total_mileage = 0
        for truck in self.trucks:
            total_mileage += truck.mileage
        return total_mileage

    def report(self):
        print(f'Current time is {CURRENT_TIME}')
        print('Total mileage for all trucks: ', self.total_truck_mileage())
        for truck in self.trucks:
            print(truck)
        for package in self.packages:
            print(package)


WgupsRoutingProgram().run()
