from package import Package


class RoutingProgramCSVParser:
    def __init__(self, file_path=None):
        self.file_path = file_path

    def parse(self):
        with open(self.file_path, 'r', encoding='utf-8-sig') as f:
            content = f.read()
            lines = self.split_string(content, '\n')
            if self.file_path.endswith('package_file.csv'):
                return self.parse_package_file(lines)
            elif self.file_path.endswith('distance_table.csv'):
                return self.parse_distance_table(lines)
            else:
                raise Exception('Invalid file path')

    # Custom split to deal with commas and newlines in quotes
    def split_string(self, string, delimiter):
        lines = []
        in_quote = False
        current_field = ''
        for char in string:
            if char == delimiter and not in_quote:
                lines.append(current_field.strip())
                current_field = ''
            elif char == '"':
                in_quote = not in_quote
                current_field += char
            else:
                current_field += char
        lines.append(current_field.strip())
        return lines

    def parse_package_file(self, lines):
        packages = []
        for line in lines[1:]:
            fields = self.split_string(line, ',')
            packages.append(Package(*fields))
        return packages

    def parse_distance_table(self, lines):
        target_addresses = []
        graph_matrix = []
        for row_idx, line in enumerate(lines[1:]):
            fields = self.split_string(line, ',')
            address = fields[1].split('\n')[0].strip(' "')
            target_addresses.append(address)

            graph_matrix.append([])
            for col_idx, field in enumerate(fields[2:]):
                if field == '':
                    break

                distance = float(field)
                graph_matrix[row_idx].append(distance)
                if distance != 0.0:
                    graph_matrix[col_idx].append(distance)
        return target_addresses, graph_matrix
