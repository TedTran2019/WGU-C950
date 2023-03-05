# Handles loading of packages into trucks
# 3 trucks, 2 drivers
class PackageManager:
    def __init__(self, packages):
        self.packages = packages


# Package 9 address is incorrect and can't be corrected until 10:20
# Packages 6, 25, 28, 32 are delayed until 9:05
# Packages 3, 18, 36, 38 can only be on truck 2
# Package 13, 14, 15, 16, 19, 20 must be delivered together
# Package 1, 6, 13, 14, 16, 20, 25, 29, 30, 31, 34, 37, 40 must be delivered by 10:30 AM
# Package 15 must be delivered by 9:00 AM


PACKAGE_9_ADDRESS = '410 S State St'
