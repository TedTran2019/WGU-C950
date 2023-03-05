from csv_parser import RoutingProgramCSVParser
from truck import Truck
from routing_graph import RoutingGraph
from package_manager import PackageManager

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
        print('Running WGUPS Routing Program')
        addresses = [package.address for package in self.packages]
        order = self.routing_graph.two_opt(addresses)
        print(order)
        # self.load_trucks()
        # self.start_delivery()


WgupsRoutingProgram().run()
