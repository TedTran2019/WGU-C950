from csv_parser import RoutingProgramCSVParser
from truck import Truck
from routing_graph import RoutingGraph
from package_manager import PackageManager
import config
from hashmap import Hashmap

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
        self.deliver_packages()
        print('WGUPS Routing Program initialized')

    def run(self):
        config.increment_global_time(500)
        self.report()

    def deliver_packages(self):
        miles1, time1 = self.deliver(self.trucks[0], config.CURRENT_TIME)
        miles2, time2 = self.deliver(self.trucks[1], config.CURRENT_TIME)
        truck_3_start_time = None
        if time1 <= time2:
            truck_3_start_time = time1
            self.trucks[0].mileage += miles1
        else:
            truck_3_start_time = time2
            self.trucks[1].mileage += miles2
        self.deliver(self.trucks[2], truck_3_start_time)

    def deliver(self, truck, time):
        self.package_manager.load_truck(truck, time)
        addresses = [package.address for package in truck.packages]
        route = self.routing_graph.two_opt(addresses)
        print(route)
        miles_to_hub, time_to_hub = truck.deliver_packages(
            route, self.routing_graph, time)
        return miles_to_hub, time_to_hub

    def total_truck_mileage(self):
        total_mileage = 0
        for truck in self.trucks:
            total_mileage += truck.mileage
        return round(total_mileage, 2)

    def report(self):
        print(f'Current time is {config.CURRENT_TIME}')
        print(
            f'Total mileage for all trucks: {self.total_truck_mileage()} miles')
        for truck in self.trucks:
            print(truck)
        for package in self.packages:
            print(package)


WgupsRoutingProgram().run()
