import json


class PlaylistManager:
    def __init__(self, filename):
        self.filename = filename


    def create_playlist(self, name):
        data = {"name": name, "tracks": []}
        file = open(self.filename, "w")
        json.dump(data, file, indent=4)
        file.close()