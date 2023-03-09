# Get is O(1) time complexity and O(1) space complexity
# Set is O(1) time complexity and O(1) space complexity
# Delete is O(1) time complexity and O(1) space complexity
class Hashmap:
    def __init__(self, num_buckets=8):
        self.store = [[] for _ in range(num_buckets)]
        self.count = 0

    # Given a key, returns the value.
    # I aliased [] to get so you can do hashmap[key] to get the value
    def get(self, key):
        for k, value in self.__bucket(key):
            if key == k:
                return value
        return None

    __getitem__ = get

    # Sets the value for a key.
    # Aliases update and []= to set so you can do hashmap[key] = value or hashmap.update(key, value)
    # Uses the private bucket method which returns the bucket for a key by hashing the key and modulo-ing it by the number of buckets
    def set(self, key, value):
        if self.count >= self.__num_buckets():
            self.__resize()
        bucket = self.__bucket(key)
        for i, kv in enumerate(bucket):
            k, _ = kv
            if key == k:
                bucket[i] = (key, value)
                return True
        bucket.append((key, value))
        self.count += 1
        return True

    __setitem__ = set
    update = set

    # Deletes a key:value pair from the hashmap
    def delete(self, key):
        bucket = self.__bucket(key)
        for i, kv in enumerate(bucket):
            k, _ = kv
            if key == k:
                del bucket[i]
                self.count -= 1
                return True
        return False

    __delitem__ = delete

    # Prints the hashmap
    def print(self):
        print("{ ", end="")
        for bucket in self.store:
            for key, value in bucket:
                print(f'{key}: {value}', end=', ')
        print("\b\b }")

    def __num_buckets(self):
        return len(self.store)

    # Doubles the number of buckets and rehashes all the keys
    def __resize(self):
        doubled = self.__num_buckets() * 2
        resized = [[] for _ in range(doubled)]
        for bucket in self.store:
            for key, value in bucket:
                resized[hash(key) % doubled].append((key, value))
        self.store = resized

    # Returns the bucket for a key by hashing the key and modulo-ing it by the number of buckets
    def __bucket(self, key):
        return self.store[hash(key) % self.__num_buckets()]
