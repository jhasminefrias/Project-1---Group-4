import os
import json
from services.basemanager import BaseManager
from data_struc.arraylist import ArrayList
from models.track import Track
from utils.sorting import Sorting

class LibraryManager(BaseManager):
    def __init__(self, filename):
        super().__init__()
        # Determine the project root reliably
        project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.filename = os.path.join(project_root, filename)

        self.tracks = ArrayList()
        self.items = self.tracks
        self.load()

    # ------------------- BASEMANAGER SHOW -------------------
    def show(self, item):
        # item is a track dict
        print(f"Now Playing: {item['title']} - {item['artist']} ({item['album']}) [{item['duration']}]")

    # ------------------- LOAD / SAVE -------------------
    def load(self):
        if not os.path.exists(self.filename):
            with open(self.filename, "w") as f:
                json.dump({"tracks": []}, f, indent=4)
        with open(self.filename, "r") as file:
            data = json.load(file)
        tracks = data.get("tracks", [])
        for t in tracks:
            self.tracks.add(t)
        self.sorting()

    def add(self, track: Track):
        self.tracks.add(track.to_dict())
        self.sorting()
        self.save()

    def delete(self, index):
        if index < 0 or index >= self.tracks.length():
            print("Invalid index!")
            return
        self.tracks.remove(index)
        self.sorting()
        self.save()
        print("Track deleted successfully.")

    def save(self):
        with open(self.filename, "w") as file:
            json.dump({"tracks": self.tracks.to_list()}, file, indent=4)

    def get_track(self, index):
        if index < 0 or index >= self.tracks.length():
            return "Invalid index"
        t = self.tracks.get(index)
        return f"{t['title']} - {t['artist']} ({t['album']}) [{t['duration']}]"

    # ------------------- SORTING -------------------
    def sorting(self):
        def clean(text):
            result = ""
            i = 0
            while i < len(text):
                if not (text[i] == " " and i > 0 and text[i-1] == " "):
                    result += text[i]
                i += 1
            return result.strip().lower()

        def to_seconds(d):
            mins, secs = d.split(":")
            return int(mins) * 60 + int(secs)

        def compare(a, b):
            titleA = clean(a["title"])
            titleB = clean(b["title"])
            artistA = clean(a["artist"])
            artistB = clean(b["artist"])
            albumA = clean(a["album"])
            albumB = clean(b["album"])

            if titleA > titleB: return 1
            if titleA < titleB: return -1
            if artistA > artistB: return 1
            if artistA < artistB: return -1
            if albumA > albumB: return 1
            if albumA < albumB: return -1

            durA = to_seconds(a["duration"])
            durB = to_seconds(b["duration"])
            if durA > durB: return 1
            if durA < durB: return -1
            return 0

        tracks_list = self.tracks.to_list()
        Sorting.bubble_sort(tracks_list, compare)

        # rebuild ArrayList
        self.tracks = ArrayList()
        for t in tracks_list:
            self.tracks.add(t)

    # ------------------- DISPLAY -------------------
    def display_tracks(self):
        if self.tracks.length() == 0:
            print("No tracks found.")
            return
        for i in range(self.tracks.length()):
            t = self.tracks.get(i)
            print(f"[{i + 1}]. {t['title']} - {t['artist']} ({t['album']}) [{t['duration']}]")
        
        