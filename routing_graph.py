from hashmap import Hashmap


# Graph represented by an adjacency matrix
# Just takes in the underlying data structure and does necesssary operations on it
class RoutingGraph:
    def __init__(self, distance_matrix, vertices):
        self.matrix = distance_matrix
        self.vertices = vertices
        self._lookup = self.create_lookup()

    def create_lookup(self):
        lookup = Hashmap()
        for i in range(len(self.vertices)):
            lookup.set(self.vertices[i], i)
        return lookup

    def lookup(self, input):
        return self._lookup[input]
