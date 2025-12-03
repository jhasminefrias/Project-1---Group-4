import json
import os
import random
from data_struc.arraylist import ArrayList
from models.track import Track


class MusicQueue:
    def __init__(self, file_path: str = None):
        self.__tracks = ArrayList()
        self.__current_index = 0
        self.__is_shuffled = False
        self.__is_repeat = False
        self.__is_playing = False
        self.__original_order = []

        project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.__file_path = file_path or os.path.join(project_root, "data", "queue_state.json")

        self.load_state()

    # ---------------- ADD TRACK ----------------
    def add_track(self, track: Track):
        for i in range(self.__tracks.length()):
            if self.__tracks.get(i) == track:
                print(f"Track '{track.title}' already in queue.")
                return False

        self.__tracks.add(track)

        if not self.__is_shuffled:
            self.__original_order.append(track)

        self.save_state()
        return True

    # ---------------- PLAYBACK ----------------
    def play(self):
        if self.__tracks.length() == 0:
            print("Queue is empty.")
            return

        self.__is_playing = True
        self.save_state()
        return self.get_current_track()

    def next_track(self):
        if self.__tracks.length() == 0:
            print("Queue is empty.")
            return

        self.__current_index += 1

        if self.__current_index >= self.__tracks.length():
            if self.__is_repeat:
                self.__current_index = 0
            else:
                self.__current_index = self.__tracks.length() - 1
                self.__is_playing = False

        self.save_state()
        return self.get_current_track()

    def previous_track(self):
        if self.__tracks.length() == 0:
            print("Queue is empty.")
            return

        self.__current_index -= 1
        if self.__current_index < 0:
            self.__current_index = 0

        self.save_state()
        return self.get_current_track()

    # ---------------- GETTERS ----------------
    def get_current_track(self):
        if self.__tracks.length() == 0:
            return None
        return self.__tracks.get(self.__current_index)

    def get_tracks(self):
        return self.__tracks.to_list()

    def get_size(self):
        return self.__tracks.length()

    def remove_track(self, index):
        if index < 0 or index >= self.__tracks.length():
            return

        self.__tracks.remove(index)

        if self.__current_index >= self.__tracks.length():
            self.__current_index = 0

        self.save_state()

    # ---------------- SAVE / LOAD ----------------
    def save_state(self):
        state = {
            "tracks": [t.to_dict() for t in self.__tracks.to_list()],
            "current_index": self.__current_index,
            "is_shuffled": self.__is_shuffled,
            "is_repeat": self.__is_repeat,
            "is_playing": self.__is_playing,
            "original_order": [t.to_dict() for t in self.__original_order]
        }

        os.makedirs(os.path.dirname(self.__file_path), exist_ok=True)

        with open(self.__file_path, "w") as f:
            json.dump(state, f, indent=4)

    def load_state(self):
        if not os.path.exists(self.__file_path):
            return

        try:
            with open(self.__file_path, "r") as f:
                state = json.load(f)

            self.__tracks = ArrayList()
            for t in state.get("tracks", []):
                self.__tracks.add(Track(t["title"], t["artist"], t["album"], t["duration"]))

            self.__current_index = state.get("current_index", 0)
            self.__is_shuffled = state.get("is_shuffled", False)
            self.__is_repeat = state.get("is_repeat", False)
            self.__is_playing = state.get("is_playing", False)

            self.__original_order = []
            for t in state.get("original_order", []):
                self.__original_order.append(Track(t["title"], t["artist"], t["album"], t["duration"]))

        except:
            print("Failed to load queue state.")