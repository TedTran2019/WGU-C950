class Package:
    def __init__(self, package_id, address, city, state, zip, deadline, mass, notes):
        self.package_id = package_id
        self.address = address
        self.city = city
        self.state = state
        self.zip = zip
        self.deadline = deadline
        self.mass = mass
        self.notes = notes

    # package_id already unique, so it works perfectly as a hash
    def __hash__(self):
        return self.package_id
