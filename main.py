from csv_parser import RoutingProgramCSVParser


class WgupsRoutingProgram:
    def __init__(self):
        print('WGU Routing Program initialized')


DISTANCE_TABLE_PATH = 'assets/distance_table.csv'
PACKAGE_TABLE_PATH = 'assets/package_file.csv'

packages = RoutingProgramCSVParser(PACKAGE_TABLE_PATH).parse()
print(packages)
