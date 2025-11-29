from data_struc.arraylist import ArrayList


class QueueDS:
    def __init__(self):
        self.items = ArrayList()


    def enqueue(self, item):
        self.items.add(item)


    def dequeue(self):
        if self.items.length() == 0:
            return None
        first = self.items.get(0)
        self.items.remove(0)
        return first


    def is_empty(self):
        return self.items.length() == 0


    def to_list(self):
        return self.items.to_list()