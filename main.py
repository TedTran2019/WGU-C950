#  Ted Tran 010534644
# __init__ calls deliver_packages which calls deliver which calls two_opt, so it's O(n^2) time and O(n) space
# create_package_hashmap is O(n) time and O(n) space
# run and set_choice are O(N * P) time and O(1) space, where N is user input and P is number of packages/trucks
# deliver_packages and deliver, like __init__ are O(n^2) time and O(n) space
# total_truck_mileage is O(n) time and O(1) space
# package_information is O(1) time and O(1) space
# report is O(n) time and O(1) space

"""
Program flow flow outline: 
1. The program begins by preparing the data for the simulation.
   a. Initializes trucks
   b. Parses package data from CSV file into a list of package objects
   c. Parses distance table from CSV file into a list of target addresses and a matrix of distances
   d. The package manager sorts the packages into lists of packages that need to be delivered by each truck
   e. The list of target addresses and matrix of distances are used to create a routing graph
2. Packages are "delivered" aka all package have delivery_time set
   a. truck 1 starts at 8:00 AM, truck 3 starts at 9:05 AM, truck 2 starts whenever a truck returns to hub
       How is this done?
       1. The package manager loads a truck with the packages it needs to deliver (which sets the package's loading_time and delivery_truck)
       2. The addresses of these packages are passed to the routing graph to get the order in which the packages should be delivered
       3. The trucks deliver the packages in the order specified by the routing graph, setting delivery_time for each package and distance_traveled for the truck
3. The package_hashmap is created to allow for quick lookup of packages by ID
   a. The list of packages is iterated through, setting each package_id as the key and the package as the value
4. The simulation is run after steps 1-3 finish preparing the necessary data
   a. The user can set the desired time to view truck/package information at
   b. Then the user can choose to view the status of all trucks/packages, or enter a package ID to view the status of a specific package 
   c. Certain components of package data are dynamically displayed based on the set time, delivery time, and loading time
"""

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
        self.package_hashmap = self.create_package_hashmap(self.packages)
        print('WGUPS Routing Program initialized')

    # This creates a hashmap of packages with the package_id as the key and the package as the value
    def create_package_hashmap(self, packages):
        package_hashmap = Hashmap()
        for package in packages:
            package_hashmap[package.package_id] = package
        return package_hashmap

    # This method returns all information for a package with the given package_id
    def package_information(self, package_id):
        package = self.package_hashmap[package_id]
        if package == None:
            print(f'\nPackage with ID {package_id} not found\n')
            return
        print(f'\nPackage ID: {package.package_id}')
        print(f'Address: {package.address}')
        print(f'Delivery deadline: {package.deadline}')
        print(f'City: {package.city}')
        print(f'Zip code: {package.zip}')
        print(f'Weight: {package.mass} kilos')
        print(f'Notes: {package.notes}')
        delivery_string = f'Delivery Status: {package.status()}'
        if package.status() == 'delivered':
            delivery_string += f' at {package.delivery_time}'
        print(delivery_string)
        print()

    # A loop so the user can set the desired time and view truck/package information at that time
    def run(self):
        while True:
            print(
                'Enter time in this format: 12:12 AM to set the desired time')
            print(
                'Enter "exit" to quit the program')
            user_input = input('Enter time: ')
            if user_input == 'exit':
                print('Exiting program...')
                break
            try:
                time = config.parse_time(user_input)
                config.set_global_time(time)
                self.set_choice()
            except ValueError:
                print('Invalid time format, please try again! [HH:MM AM/PM]')

    # Allows the user to choose to see the status of all trucks/packages or the status of a specific package
    def set_choice(self):
        while True:
            print('Enter 1 to see the status of all trucks/packages')
            print('Enter 2 to see all the information for a specific package')
            choice = input('Enter choice: ')
            if choice == '1':
                self.report()
                break
            elif choice == '2':
                try:
                    print('Enter the package ID')
                    package_id = int(input('Enter ID: '))
                    self.package_information(package_id)
                    break
                except ValueError:
                    print('Invalid package ID, please try again!')
            else:
                print('Invalid choice, please try again!')

    # This method has the 1st truck deliver packages at 8:00 AM
    # The 3rd truck delivers packages at 9:05 AM
    # The 2nd truck delivers packages whenever a truck returns to the hub
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

    # This is a helper method that loads a truck, gets the route for the truck, and delivers the packages
    def deliver(self, truck, time):
        self.package_manager.load_truck(truck, time)
        addresses = [package.address for package in truck.packages]
        route = self.routing_graph.two_opt(addresses)
        miles_to_hub, time_to_hub = truck.deliver_packages(
            route, self.routing_graph, time)
        return miles_to_hub, time_to_hub

    # This method returns the total mileage for all trucks
    def total_truck_mileage(self):
        total_mileage = 0
        for truck in self.trucks:
            total_mileage += truck.current_mileage()
        return round(total_mileage, 2)

    # This method prints the current time, total mileage for all trucks, and the status of all trucks/packages at the current time
    def report(self):
        print(f'\nCurrent time is {config.CURRENT_TIME}')
        print(
            f'Total mileage for all trucks: {self.total_truck_mileage()} miles')
        for truck in self.trucks:
            print(truck)
        for package in self.packages:
            print(package)
        print()


WgupsRoutingProgram().run()
