import config
from hashmap import Hashmap


class Truck:
    def __init__(self, truck_id, capacity=16, speed=18):
        self.truck_id = truck_id
        self.start_time = None
        self.end_time = None
        self.packages = []
        self.current_location = 'HUB'
        self.capacity = capacity
        self.speed = speed
        self.mileage = 0

    def __str__(self):
        return f'Truck {self.truck_id} is at {self.current_location} having travelled {self.mileage} miles'

    # address -> array of packages
    def setup_package_hashmap(self):
        package_hashmap = Hashmap()
        for package in self.packages:
            if package_hashmap[package.address]:
                package_hashmap[package.address].append(package)
            else:
                package_hashmap[package.address] = [package]
        return package_hashmap

    def deliver_packages(self, order_list, routing_graph):
        if not self.packages:
            print('No packages to deliver')
            return

        self.start_time = config.CURRENT_TIME
        time = config.CURRENT_TIME
        package_hashmap = self.setup_package_hashmap()
        for i in range(1, len(order_list) - 1):
            current_address = order_list[i - 1]
            target_address = order_list[i]
            distance = routing_graph.get_distance(
                current_address, target_address)
            time = config.increment_time(
                time, self.calculate_time_elapsed_in_minutes(distance))
            self.mileage += distance
            for package in package_hashmap[routing_graph.vertices[target_address]]:
                package.delivery_time = time

    def calculate_time_elapsed_in_minutes(self, distance):
        return distance / self.speed * 60
