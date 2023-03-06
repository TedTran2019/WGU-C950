import config


class Package:
    def __init__(self, package_id, address, city, state, zip, deadline, mass, notes):
        self.package_id = int(package_id)
        self.address = address
        self.city = city
        self.state = state
        self.zip = zip
        self.deadline = deadline if deadline == 'EOD' else config.parse_time(
            deadline)
        self.mass = mass
        self.notes = notes
        self.status = 'at the hub'
        self.delivery_time = None
        self.delivery_truck = None
        self.delayed_until = None

    # package_id already unique, so it works perfectly as a hash
    def __hash__(self):
        return self.package_id

    def __str__(self):
        string = f'Package {self.package_id} is {self.status}'
        if self.delivery_truck == None:
            string += ' and is waiting to be loaded onto a truck'
        elif self.delivery_time >= config.CURRENT_TIME:
            string += f' at {self.delivery_time} by truck {self.delivery_truck} to {self.address}'
        elif self.delivery_time < config.CURRENT_TIME:
            string += f' by truck {self.delivery_truck} to {self.address}'
        elif self.delayed_until != None and self.delayed_until >= config.CURRENT_TIME:
            string += f' and delayed until {self.delayed_until}'
        if self.deadline != 'EOD':
            string += f' with a deadline of {self.deadline}'
        return string

    def deliver(self, delivery_time):
        self = self.delivery_time


STATUSES = ['at the hub', 'en route', 'delivered']
