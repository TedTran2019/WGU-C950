# setup_package_hashmap is O(n) time complexity and O(n) space complexity
# deliver packages is O(n) time complexity and O(n) space complexity
# Everything else is O(1) time complexity and O(1) space complexity

import config
from hashmap import Hashmap


class Truck:
    def __init__(self, truck_id, capacity=16, speed=18):
        self.truck_id = truck_id
        self.start_time = None
        self.packages = []
        self.capacity = capacity
        self.speed = speed
        self.mileage = 0

    # Outputs the truck's id and current mileage when the prind method is called on it
    def __str__(self):
        return f'Truck {self.truck_id} has travelled {round(self.current_mileage(), 2)} miles'

    # address -> array of packages
    # Creates a hashmap where the key is the address and the value is an array of packages
    def setup_package_hashmap(self):
        package_hashmap = Hashmap()
        for package in self.packages:
            if package_hashmap[package.address]:
                package_hashmap[package.address].append(package)
            else:
                package_hashmap[package.address] = [package]
        return package_hashmap

    # Given the route, routing_graph, and start_time
    # It "delivers" all the packages by setting their delivery time
    # Also updates the truck's mileage
    # It returns the distance to the hub and the time to the hub, so the truck with the shorter path can return to hub
    def deliver_packages(self, order_list, routing_graph, start_time):
        if not self.packages:
            print('No packages to deliver')
            return

        self.start_time = start_time
        time = start_time
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

        miles_to_hub = routing_graph.get_distance(
            order_list[-2], order_list[-1])
        time_to_hub = config.increment_time(
            time, self.calculate_time_elapsed_in_minutes(miles_to_hub))
        return miles_to_hub, time_to_hub

    # Calculates the time elapsed in minutes from distance travelled and truck speed
    def calculate_time_elapsed_in_minutes(self, distance):
        return distance / self.speed * 60

    # Returns the current mileage of the truck based on current time
    def current_mileage(self):
        if self.start_time == None or config.CURRENT_TIME <= self.start_time:
            return 0

        time_elapsed = config.subtract_times(
            config.CURRENT_TIME, self.start_time)
        distance = self.speed * time_elapsed.seconds / 3600
        if distance >= self.mileage:
            return self.mileage
        else:
            return distance
