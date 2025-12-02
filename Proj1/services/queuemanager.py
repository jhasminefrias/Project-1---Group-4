from services.basemanager import BaseManager
from data_struc.arraylist import ArrayList
from utils.pagination import paginate
from services.libmanager import LibraryManager

class QueueManager(BaseManager):
    def __init__(self):
        super().__init__()
        self.queue = ArrayList()  # stores all tracks in queue
        self.items = self.queue   # for BaseManager playback
        self.current_index = 0    # tracks current playing position
        self.library = LibraryManager("data/library.json")

    # ------------------- ADD TRACK TO QUEUE -------------------
    def add_to_queue_from_library_or_manual(self, library_manager):
        print("Do you want to add track from library or manually?")
        choice = input("Enter 'l' for library, 'm' for manual: ").strip().lower()
        
        if choice == 'l':
            page = 1
            tracks = self.library.tracks.to_list()
            paginate(tracks, page=page, page_size=10, title="LIBRARY TRACKS")
            # library_manager.display_tracks()
            try:
                index = int(input("Enter track number to add: ")) - 1
                track_dict = library_manager.tracks.get(index)
            except:
                print("Invalid track number.")
                return
            self.queue.add(track_dict)
            print(f"Added '{track_dict['title']}' to the queue.")
        
        elif choice == 'm':
            title = input("Track title: ")
            artist = input("Artist: ")
            album = input("Album: ")
            duration = input("Duration (mm:ss): ")
            t_dict = {"title": title, "artist": artist, "album": album, "duration": duration}
            self.queue.add(t_dict)
            print(f"Added '{title}' to the queue.")
        else:
            print("Invalid choice.")

    # ------------------- DISPLAY QUEUE -------------------
    def display_queue(self):
        if self.queue.length() == 0:
            print("Queue is empty.")
            return
        print("Queue:")
        for i in range(self.queue.length()):
            t = self.queue.get(i)
            marker = ">>" if i == self.current_index else "  "
            print(f"{marker} {i + 1}. {t['title']} - {t['artist']} ({t['album']}) [{t['duration']}]")

    # ------------------- PLAYBACK -------------------
    def play_current(self):
        if self.queue.length() == 0:
            print("Queue is empty.")
            return
        t = self.queue.get(self.current_index)
        print(f"Now Playing: {t['title']} - {t['artist']} ({t['album']}) [{t['duration']}]")

    def next_track(self):
        if self.queue.length() == 0:
            print("Queue is empty.")
            return
        self.current_index += 1
        if self.current_index >= self.queue.length():
            self.current_index = 0
        self.play_current()

    def previous_track(self):
        if self.queue.length() == 0:
            print("Queue is empty.")
            return
        self.current_index -= 1
        if self.current_index < 0:
            self.current_index = self.queue.length() - 1
        self.play_current()

    def remove_track(self):
        if self.queue.length() == 0:
            print("Queue is empty.")
            return

        self.display_queue()
        try:
            index = int(input("Enter track number to remove: ")) - 1
            removed = self.queue.get(index)
            self.queue.remove(index)

            # Adjust current_index if needed
            if index < self.current_index:
                self.current_index -= 1
                print("List is Empty!")
            elif index == self.current_index:
                # Keep current_index in bounds
                if self.current_index >= self.queue.length():
                    self.current_index = 0

            print(f"Removed '{removed['title']}' from the queue.")

        except (IndexError, ValueError):
            print("Invalid track number.")
