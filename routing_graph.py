# two_opt is O(n^2) time and O(n) space
# create_lookup is O(n) time and O(n) space
# tour_distance is O(n) time and O(1) space
# Everything else is O(1) time and O(1) space
from hashmap import Hashmap


# Graph represented by an adjacency matrix
class RoutingGraph:
    def __init__(self, distance_matrix, vertices):
        self.matrix = distance_matrix
        self.vertices = vertices
        self._lookup = self.create_lookup()

    # Creates a hashmap of the vertices and their indices
    def create_lookup(self):
        lookup = Hashmap()
        for i in range(len(self.vertices)):
            lookup.set(self.vertices[i], i)
        return lookup

    # Returns the index of the vertex (address)
    def lookup(self, input):
        return self._lookup[input]

    # Returns the total distance between all vertices in the tour
    def tour_distance(self, tour):
        total_distance = 0
        for i in range(len(tour) - 1):
            total_distance += self.get_distance(tour[i], tour[i + 1])
        return total_distance

    # Returns the distance between two addresses
    def get_distance_by_address(self, address1, address2):
        return self.matrix[self.lookup(address1)][self.lookup(address2)]

    # Returns the distance between two indices
    def get_distance(self, index1, index2):
        return self.matrix[index1][index2]

    # Starts from hub and returns to hub; when actually utilizing the results,
    # abandon the truck once all packages are delivered
    # This is the 2-opt algorithm which swaps two edges in a tour repeatedly until no shorter tour can be found
    def two_opt(self, addresses, starting_index=0):
        tour = [starting_index] + \
            [self.lookup(address) for address in addresses]
        tour.append(starting_index)
        n = len(tour)
        min_tour_distance = self.tour_distance(tour)
        improved = True
        while improved:
            improved = False
            for i in range(1, n - 2):
                for j in range(i + 1, n):
                    new_tour = tour[:]
                    new_tour[i:j] = tour[j - 1:i - 1:-1]
                    new_distance = self.tour_distance(new_tour)
                    if new_distance < min_tour_distance:
                        tour = new_tour
                        min_tour_distance = new_distance
                        improved = True
            if not improved:
                break
        return tour
