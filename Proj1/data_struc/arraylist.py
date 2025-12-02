#so, ang pinaka first nato huna-hunaon is, unsay purpose sa class arraylist?
#since it was written sa pdf nga bawal daw ang most built in function, we need to create our own array to serve as our backbone data struc
#kaning arraylist, resizable array ni sha nga mo double iyahang capacity (size) if mapuno na

class ArrayList:
    def __init__(self, capacity=10):    #---> the capacity serves as the space allocated for this array, in this case 10 sa ang default
        self.capacity = capacity
        self.size = 0                   #----> ang size kay mao na siya mismo ang kung pilay elements ang naka store
        self.data = [None] * self.capacity

    def add(self, item):                #kaning add method, mao ni sha atong magamit if mag add ta ug mga tracks later, reusable ni siya
        if self.size == self.capacity:
            self._resize()
        self.data[self.size] = item
        self.size += 1

    def _resize(self):
        new_capacity = self.capacity * 2
        new_data = [None] * new_capacity
        for i in range(self.size):
            new_data[i] = self.data[i]
        self.data = new_data
        self.capacity = new_capacity

    def get(self, index):
        if index < 0 or index >= self.size:
            raise IndexError("Index out of bounds")
        return self.data[index]

    def set(self, index, item):
        if index < 0 or index >= self.size:
            raise IndexError("Index out of bounds")
        self.data[index] = item

    def remove(self, index):
        if index < 0 or index >= self.size:
            raise IndexError("Index out of bounds")
        for i in range(index, self.size - 1):
            self.data[i] = self.data[i + 1]
        self.data[self.size - 1] = None
        self.size -= 1

    def length(self):
        return self.size

    def to_list(self):          #---> meant for returning the exact amount(size) of elements, para di na maapil ang None elements. 
        return self.data[:self.size]            # but it can also be used to convert the object's content into a standard list para sa display purposes

    def contains(self, item):       #---> this is js for checking if naay duplicates
        for i in range(self.size):
            if self.data[i] == item:
                return True
        return False

    def index_of(self, item):
        for i in range(self.size):
            if self.data[i] == item:
                return i
        return -1
    
    def clear(self):
        for i in range(self.size):
            self.data[i] = None
        self.size = 0
