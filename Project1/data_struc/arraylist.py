class ArrayList:
    def __init__(self, capacity=10):
        self.capacity = capacity
        self.size = 0
        self.data = [None] * self.capacity


    def add(self, item):
        if self.size == self.capacity:
            self._resize()
        self.data[self.size] = item
        self.size += 1


    def _resize(self):
        new_capacity = self.capacity * 2
        new_data = [None] * new_capacity
        i = 0
        while i < self.size:
            new_data[i] = self.data[i]
            i += 1
        self.data = new_data
        self.capacity = new_capacity


    def get(self, index):
        if index < 0 or index >= self.size:
            raise IndexError("Index out of bounds")
        return self.data[index]


    def remove(self, index):
        if index < 0 or index >= self.size:
            raise IndexError("Index out of bounds")
        i = index
        while i < self.size - 1:
            self.data[i] = self.data[i + 1]
            i += 1
        self.data[self.size - 1] = None
        self.size -= 1


    def length(self):
        return self.size


    def to_list(self):
        result = []
        i = 0
        while i < self.size:
            result += [self.data[i]]
            i += 1

        return result
