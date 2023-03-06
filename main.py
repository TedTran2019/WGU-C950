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
        while True:
            print(
                'Enter time in this format: 12:12 AM to see the status of all trucks/packages at that time!')
            print('Enter "exit" to quit the program')
            user_input = input('Enter time: ')
            if user_input == 'exit':
                print('Exiting program...')
                break
            try:
                time = config.parse_time(user_input)
                config.set_global_time(time)
                self.report()
            except ValueError:
                print('Invalid time format, please try again! [HH:MM AM/PM]')

    def deliver_packages(self):
        miles1, time1 = self.deliver(self.trucks[0], config.CURRENT_TIME)
        miles3, time3 = self.deliver(
            self.trucks[2], config.parse_time('9:05 AM'))
        truck_2_start_time = None
        if time1 <= time3:
            truck_2_start_time = time1
            self.trucks[0].mileage += miles1
        else:
            truck_2_start_time = time3
            self.trucks[2].mileage += miles3
        self.deliver(self.trucks[1], truck_2_start_time)

    def deliver(self, truck, time):
        self.package_manager.load_truck(truck, time)
        addresses = [package.address for package in truck.packages]
        route = self.routing_graph.two_opt(addresses)
        miles_to_hub, time_to_hub = truck.deliver_packages(
            route, self.routing_graph, time)
        return miles_to_hub, time_to_hub

    def total_truck_mileage(self):
        total_mileage = 0
        for truck in self.trucks:
            total_mileage += truck.current_mileage()
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
