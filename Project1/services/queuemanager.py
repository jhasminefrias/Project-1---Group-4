import json
from data_struc.queueDS import QueueDS


class QueueManager:
    def __init__(self, filename):
        self.filename = filename
        self.queue = QueueDS()


    def add_to_queue(self, track):
        self.queue.enqueue(track)
        self.save()


    def save(self):
        file = open(self.filename, "w")
        json.dump({"queue": self.queue.to_list()}, file, indent=4)
        file.close()