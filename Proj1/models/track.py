class Track:
    def __init__(self, title, artist, album, duration):
        self.title = title
        self.artist = artist
        self.album = album
        self.duration = duration

    def to_dict(self):
        return {
            "title": self.title,
            "artist": self.artist,
            "album": self.album,
            "duration": self.duration
        }

    def __eq__(self, other):
        if isinstance(other, Track):
            return (self.title == other.title and self.artist == other.artist and
                    self.album == other.album and self.duration == other.duration)
        return False
