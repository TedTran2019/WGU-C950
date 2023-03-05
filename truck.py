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
