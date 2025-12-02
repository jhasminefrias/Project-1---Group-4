from data_struc.arraylist import ArrayList

class BaseManager:
    def __init__(self):
        self.current_index = -1
        self.items = ArrayList()  # Ensure items exist

    def play(self, index):
        if index < 0 or index >= self.items.length():
            print("Invalid item number.")
            return
        self.current_index = index
        item = self.items.get(self.current_index)
        self.show(item)

    def next(self):
        if self.items.length() == 0:
            print("No items available.")
            return
        if self.current_index == -1:
            self.current_index = 0
        else:
            self.current_index += 1
        if self.current_index >= self.items.length():
            self.current_index = self.items.length() - 1
            print("Reached end.")
            return
        self.show(self.items.get(self.current_index))

    def previous(self):
        if self.current_index <= 0:
            print("No previous item.")
            return
        self.current_index -= 1
        self.show(self.items.get(self.current_index))

    def stop(self):
        if self.current_index == -1:
            print("Nothing is playing.")
        else:
            print("Stopped.")
            self.current_index = -1

    def show(self, item):
        raise NotImplementedError()
