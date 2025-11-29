import json
from data_struc.arraylist import ArrayList
from models.track import Track


class LibraryManager:
    def __init__(self, filename):
        self.filename = filename
        self.tracks = ArrayList()
        self.load()


    def load(self):
        try:
            file = open(self.filename, "r")
            data = json.load(file)
            file.close()

            tracks = data.get("tracks", [])
            i = 0
            while i < len(tracks):
                self.tracks.add(tracks[i])
                i += 1

        except FileNotFoundError:
            # Only create the file if it truly does not exist
            file = open(self.filename, "w")
            file.write('{"tracks": []}')
            file.close()

        except json.JSONDecodeError:
            print("ERROR: library.json is corrupted. Fix the JSON file manually.")
            # IMPORTANT: Do NOT overwrite file here

        except Exception as e:
            print("Unexpected error while loading:", e)
            # IMPORTANT: Do NOT overwrite file


    def add(self, track: Track):
        self.tracks.add(track.to_dict())
        self.save()
        print("Saving to:", self.filename)



    def save(self):
        file = open(self.filename, "w")
        json.dump({"tracks": self.tracks.to_list()}, file, indent=4)
        file.close()


    def display_tracks(self):
        i = 0
        while i < self.tracks.length():
            t = self.tracks.get(i)
            print(f"{t['title']} - {t['artist']} ({t['album']}) [{t['duration']}]")
            i += 1