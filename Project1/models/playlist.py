from data_struc.arraylist import ArrayList

class Playlist:
    def __init__(self, name):
        self.name = name
        self.tracks = ArrayList()


    def add_track(self, track):
        self.tracks.add(track)