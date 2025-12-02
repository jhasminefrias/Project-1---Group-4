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

        project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))      #this points to the root directory sa atong project
        self.__file_path = file_path or os.path.join(project_root, "data", "queue_state.json")

    def add_track(self, track: Track):
        for i in range(self.__tracks.length()):
            if self.__tracks.get(i) == track:
                print(f"Track '{track.title}' already in queue.")
                return False
        self.__tracks.add(track)
        if not self.__is_shuffled:
            self.__original_order.append(track)
        return True

    def load_tracks(self, tracks):
        for t in tracks:
            self.add_track(t)
        self.save_state()

    def play(self):
        if self.__tracks.length() == 0:
            return
        if not self.__is_repeat and self.__current_index >= self.__tracks.length():
            self.__current_index = 0
        self.__is_playing = True
        self.save_state()

    def pause(self):
        self.__is_playing = False
        self.save_state()

    def next_track(self):
        if self.__tracks.length() == 0:
            return None
        if self.__current_index + 1 < self.__tracks.length():
            self.__current_index += 1
        elif self.__is_repeat:
            self.__current_index = 0
        else:
            self.__is_playing = False
            self.save_state()
            return None
        self.save_state()
        return self.get_current_track()

    def previous_track(self):
        if self.__tracks.length() == 0:
            return None
        if self.__current_index > 0:
            self.__current_index -= 1
        elif self.__is_repeat:
            self.__current_index = self.__tracks.length() - 1
        self.save_state()
        return self.get_current_track()

    def shuffle(self):
        n = self.__tracks.length()
        if self.__is_shuffled or n <= 1:
            return
        if len(self.__original_order) == 0:
            self.__original_order = self.__tracks.to_list()
        current = self.get_current_track()
        lst = self.__tracks.to_list()
        random.shuffle(lst)
        self.__tracks = ArrayList()
        for t in lst:
            self.__tracks.add(t)
        for i in range(self.__tracks.length()):
            if self.__tracks.get(i) == current:
                self.__current_index = i
                break
        self.__is_shuffled = True
        self.save_state()

    def unshuffle(self):
        if not self.__is_shuffled:
            return
        current = self.get_current_track()
        new_tracks = [t for t in self.__tracks.to_list() if t not in self.__original_order]
        self.__tracks = ArrayList()
        for t in self.__original_order:
            self.__tracks.add(t)
        for t in new_tracks:
            self.__tracks.add(t)
            self.__original_order.append(t)
        for i in range(self.__tracks.length()):
            if self.__tracks.get(i) == current:
                self.__current_index = i
                break
        self.__is_shuffled = False
        self.save_state()

    def toggle_repeat(self):
        self.__is_repeat = not self.__is_repeat
        self.save_state()
        return self.__is_repeat

    def clear(self):
        self.__tracks = ArrayList()
        self.__current_index = 0
        self.__is_shuffled = False
        self.__is_repeat = False
        self.__is_playing = False
        self.__original_order = []
        self.save_state()

    def get_current_track(self):
        if self.__tracks.length() == 0:
            return None
        return self.__tracks.get(self.__current_index)

    def get_tracks(self):
        return self.__tracks.to_list()

    def get_size(self):
        return self.__tracks.length()

    def is_playing(self):
        return self.__is_playing

    def is_shuffled(self):
        return self.__is_shuffled

    def is_repeat_on(self):
        return self.__is_repeat

    def get_total_duration(self):
        total_seconds = 0
        for t in self.__tracks.to_list():
            try:
                d = t.duration
                if isinstance(d, int):
                    seconds = d
                else:
                    if ":" in str(d):
                        mins, secs = str(d).split(":")
                        seconds = int(mins) * 60 + int(secs)
                    else:
                        seconds = int(d)
            except:
                seconds = 0
            total_seconds += seconds
        hours = total_seconds // 3600
        minutes = (total_seconds % 3600) // 60
        return f"{hours} hr {minutes} min"

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
            return False
        try:
            with open(self.__file_path, "r") as f:
                state = json.load(f)
            self.__tracks = ArrayList()
            for t in state["tracks"]:
                self.__tracks.add(Track(t["title"], t["artist"], t["album"], t["duration"]))
            self.__current_index = state["current_index"]
            self.__is_shuffled = state["is_shuffled"]
            self.__is_repeat = state["is_repeat"]
            self.__is_playing = state["is_playing"]
            self.__original_order = [Track(t["title"], t["artist"], t["album"], t["duration"]) for t in state["original_order"]]
            return True
        except:
            return False
