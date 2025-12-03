import os
import sys

# Ensure project root is on sys.path so sibling packages like data_struc
# can be imported when this file is executed directly or from different CWDs.
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

import json
from data_struc.queueDS import MusicQueue


class QueueManager:
    def __init__(self, filename):
        self.filename = filename
        # Use MusicQueue to manage its own state file (queue_state.json by default)
        self.queue = MusicQueue()
        # load existing state if present
        try:
            self.queue.load_state()
        except Exception:
            # fail silently; queue will start empty
            pass


    def add_to_queue(self, track):
        # use MusicQueue.add_track and persist using its save_state
        added = self.queue.add_track(track)
        if added:
            try:
                self.queue.save_state()
            except Exception:
                pass
        return added


    def save(self):
        # Persist using the MusicQueue's own save method
        try:
            self.queue.save_state()
        except Exception:
            # fallback: write a minimal file to self.filename if needed
            try:
                with open(self.filename, "w") as f:
                    json.dump(
                        {"tracks": [t.to_dict() for t in self.queue.get_tracks()]},
                        f,
                        indent=4
                    )
            except Exception:
                pass


# from services.basemanager import BaseManager
# from utils.pagination import paginate
# from services.libmanager import LibraryManager
# from data_struc.queueDS import MusicQueue
# from models.track import Track
# import json


# class QueueManager(BaseManager):
#     def __init__(self):
#         super().__init__()
#         self.queue = MusicQueue()     # ✅ USE MusicQueue
#         self.library = LibraryManager("data/library.json")

#     # ---------------- ADD TRACK TO QUEUE ----------------
#     def add_to_queue_from_library_or_manual(self, library_manager):
#         print("Do you want to add track from library or manually?")
#         choice = input("Enter 'l' for library, 'm' for manual: ").strip().lower()

#         # ---------- FROM LIBRARY ----------
#         if choice == 'l':
#             page = 1
#             tracks = library_manager.tracks.to_list()

#             paginate(tracks, page=page, page_size=10, title="LIBRARY TRACKS")
#             # with open ("data/queue_state.json", "w") as file:
#             #     # data = json.dump(file, )
#             #     json.dump({"tracks": tracks}, "data/queue_state.json", indent=4)


#             try:
#                 index = int(input("Enter track number to add: ")) - 1
#                 track = library_manager.tracks.get(index)

#                 self.save("Proj1/data/queue_state.json", track)
#                 if isinstance(track, Track):
#                     self.queue.add_track(track)
#                     # self.save("Proj1/data/queue_state.json", track)
#                     print(f"Added '{track.title}' to the queue.")
#                 else:
#                     print("Invalid track.")

#             except:
#                 print("Invalid track number.")

#         # ---------- MANUAL ----------
#         elif choice == 'm':
#             title = input("Track title: ")
#             artist = input("Artist: ")
#             album = input("Album: ")
#             duration = input("Duration (mm:ss): ")

#             track = Track(title, artist, album, duration)
#             self.queue.add_track(track)

#             print(f"Added '{title}' to the queue.")

#         else:
#             print("Invalid choice.")

#     # ---------------- DISPLAY QUEUE ----------------
#     def display_queue(self):
#         tracks = self.queue.get_tracks()

#         if not tracks:
#             print("Queue is empty.")
#             return

#         for i, t in enumerate(tracks):
#             marker = ">>" if i == self.queue._MusicQueue__current_index else "  "
#             print(f"{marker} {i + 1}. {t.title} - {t.artist} ({t.album}) [{t.duration}]")

#     def save(self, file, track):
#         with open (file, "w") as file:
#             json.dump({"tracks": track}, file, indent=4)

#     # ---------------- PLAYBACK ----------------
#     def play_current(self):
#         track = self.queue.get_current_track()

#         if not track:
#             print("Queue is empty.")
#             return

#         print(f"Now Playing: {track.title} - {track.artist} ({track.album}) [{track.duration}]")

#     def next_track(self):
#         track = self.queue.next_track()

#         if track:
#             print(f"Now Playing: {track.title} - {track.artist} ({track.album}) [{track.duration}]")

#     def previous_track(self):
#         track = self.queue.previous_track()

#         if track:
#             print(f"Now Playing: {track.title} - {track.artist} ({track.album}) [{track.duration}]")

#     # ---------------- REMOVE TRACK ----------------
#     def remove_track(self):
#         tracks = self.queue.get_tracks()

#         if not tracks:
#             print("Queue is empty.")
#             return

#         self.display_queue()

#         try:
#             index = int(input("Enter track number to remove: ")) - 1
#             removed = tracks[index]

#             self.queue.remove_track(index)

#             print(f"Removed '{removed.title}' from the queue.")

#         except:
#             print("Invalid track number.")
