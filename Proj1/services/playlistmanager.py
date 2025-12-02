from data_struc.arraylist import ArrayList
from services.basemanager import BaseManager
import json
import os
from models.track import Track

class PlaylistManager(BaseManager):
    def __init__(self, filename):
        super().__init__()
        project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.filename = os.path.join(project_root, filename)

        self.playlists = ArrayList()   # stores all playlists
        self.tracks = ArrayList()      # for BaseManager playback
        self.items = self.tracks
        self.name = None

        self.load_playlists()

    # ------------------- BASEMANAGER SHOW -------------------
    def show(self, item):
        # item is a track dict
        print(f"Now Playing: {item['title']} - {item['artist']} ({item['album']}) [{item['duration']}]")

    # ------------------- LOAD / SAVE -------------------
    def load_playlists(self):
        if not os.path.exists(self.filename):
            with open(self.filename, "w") as f:
                json.dump({"playlists": []}, f, indent=4)
        with open(self.filename, "r") as file:
            data = json.load(file)
        all_playlists = data.get("playlists", [])
        self.playlists = ArrayList()
        for pl in all_playlists:
            self.playlists.add(pl)

    def save_playlists(self):
        with open(self.filename, "w") as file:
            json.dump({"playlists": self.playlists.to_list()}, file, indent=4)

    # ------------------- PLAYLIST OPERATIONS -------------------
    def create_playlist(self, name):
        for i in range(self.playlists.length()):
            if self.playlists.get(i)["name"] == name:
                print("Playlist already exists.")
                return
        self.playlists.add({"name": name, "tracks": []})
        self.save_playlists()
        print(f"Playlist '{name}' created.")

    def delete_playlist(self, name):
        new_list = ArrayList()
        found = False
        for i in range(self.playlists.length()):
            if self.playlists.get(i)["name"] != name:
                new_list.add(self.playlists.get(i))
            else:
                found = True
        if not found:
            print("Playlist not found.")
            return
        self.playlists = new_list
        self.save_playlists()
        print(f"Playlist '{name}' deleted successfully.")

    def rename_playlist(self, old_name, new_name):
        found = False
        for i in range(self.playlists.length()):
            if self.playlists.get(i)["name"] == old_name:
                self.playlists.get(i)["name"] = new_name
                found = True
        if not found:
            print("Playlist not found.")
            return
        self.save_playlists()
        print(f"Playlist renamed from '{old_name}' to '{new_name}'")

    # ------------------- OPEN PLAYLIST -------------------
    def open_playlist(self, name):
        found = False
        for i in range(self.playlists.length()):
            if self.playlists.get(i)["name"] == name:
                self.name = name
                self.tracks = ArrayList()
                self.items = self.tracks
                for t in self.playlists.get(i)["tracks"]:
                    self.tracks.add(t)
                found = True
                break
        if not found:
            print("Playlist not found.")

    # ------------------- TRACK OPERATIONS -------------------
    def add_track(self, track: Track):
        if self.name is None:
            print("Open a playlist first.")
            return
        t_dict = track.to_dict()
        if self.tracks.contains(t_dict):
            print("Track already in playlist.")
            return
        self.tracks.add(t_dict)

        # update main playlist
        for i in range(self.playlists.length()):
            if self.playlists.get(i)["name"] == self.name:
                self.playlists.get(i)["tracks"] = self.tracks.to_list()
                break

        self.save_playlists()
        print(f"Track '{track.title}' added to playlist '{self.name}'.")

    # ------------------- DISPLAY ALL PLAYLISTS -------------------
    def display_all_playlists(self):
        if self.playlists.length() == 0:
            print("No playlists available.")
            return
        print("Playlists:")
        for i in range(self.playlists.length()):
            pl = self.playlists.get(i)
            track_count = len(pl.get("tracks", []))
            print(f"{i + 1}. {pl['name']} - {track_count} track(s)")
    
    # ------------------- DISPLAY TRACKS -------------------
    def display_tracks(self):
        if self.name is None:
            print("Open a playlist first.")
            return
        if self.tracks.length() == 0:
            print(f"No tracks in playlist '{self.name}'.")
            return
        print(f"Tracks in '{self.name}':")
        for i in range(self.tracks.length()):
            t = self.tracks.get(i)
            print(f"{i + 1}. {t['title']} - {t['artist']} ({t['album']}) [{t['duration']}]")

