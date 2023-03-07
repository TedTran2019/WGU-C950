# Get is O(1) time complexity and O(1) space complexity
# Set is O(1) time complexity and O(1) space complexity
# Delete is O(1) time complexity and O(1) space complexity
class Hashmap:
    def __init__(self, num_buckets=8):
        self.store = [[] for _ in range(num_buckets)]
        self.count = 0

    def get(self, key):
        for k, value in self.__bucket(key):
            if key == k:
                return value
        return None

    __getitem__ = get

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

    def print(self):
        print("{ ", end="")
        for bucket in self.store:
            for key, value in bucket:
                print(f'{key}: {value}', end=', ')
        print("\b\b }")

    def __num_buckets(self):
        return len(self.store)

    def __resize(self):
        doubled = self.__num_buckets() * 2
        resized = [[] for _ in range(doubled)]
        for bucket in self.store:
            for key, value in bucket:
                resized[hash(key) % doubled].append((key, value))
        self.store = resized

    def __bucket(self, key):
        return self.store[hash(key) % self.__num_buckets()]
