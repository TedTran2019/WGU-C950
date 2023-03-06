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
        self.delivery_time = None
        self.delivery_truck = None
        self.delayed_until = None
        self.loaded_at = None

    # package_id already unique, so it works perfectly as a hash
    def __hash__(self):
        return self.package_id

    def __str__(self):
        string = f'Package {self.package_id} is {self.status()}'
        if config.CURRENT_TIME < self.loaded_at:
            string += ' and is waiting to be loaded onto a truck'
        elif config.CURRENT_TIME >= self.delivery_time:
            string += f' at {self.delivery_time} by truck {self.delivery_truck} to {self.address}'
        elif config.CURRENT_TIME < self.delivery_time:
            string += f' by truck {self.delivery_truck} to {self.address}'
        elif self.delayed_until != None and config.CURRENT_TIME < self.delayed_until:
            string += f' and delayed until {self.delayed_until}'
        if self.deadline != 'EOD':
            string += f' with a deadline of {self.deadline}'
        return string

    def deliver(self, delivery_time):
        self = self.delivery_time

    def status(self):
        if config.CURRENT_TIME < self.loaded_at:
            return STATUSES[0]
        elif config.CURRENT_TIME >= self.delivery_time:
            return STATUSES[2]
        elif config.CURRENT_TIME < self.delivery_time:
            return STATUSES[1]


STATUSES = ['at the hub', 'en route', 'delivered']
