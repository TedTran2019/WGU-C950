class Package:
    def __init__(self, package_id, address, city, state, zip, deadline, mass, notes):
        self.package_id = int(package_id)
        self.address = address
        self.city = city
        self.state = state
        self.zip = zip
        self.deadline = deadline
        self.mass = mass
        self.notes = notes
        self.status = 'HUB'
        self.delivery_time = None
        self.delivery_truck = None
        self.delayed_until = None

    # package_id already unique, so it works perfectly as a hash
    def __hash__(self):
        return self.package_id

    def __str__(self):
        return f'Package {self.package_id}'
        # return f'Package {self.package_id} {self.address} {self.city} {self.state} {self.zip} {self.deadline} {self.mass} {self.notes} {self.status} {self.delivery_time} {self.delivery_truck}'


STATUSES = ['HUB', 'TRUCK', 'DELIVERED']
