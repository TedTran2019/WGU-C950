from csv_parser import RoutingProgramCSVParser


class WgupsRoutingProgram:
    def __init__(self):
        print('WGUPS Routing Program initialized')

    def run(self):
        print('Hi bye')


DISTANCE_TABLE_PATH = 'assets/distance_table.csv'
PACKAGE_TABLE_PATH = 'assets/package_file.csv'

packages = RoutingProgramCSVParser(PACKAGE_TABLE_PATH).parse()
print(packages)
