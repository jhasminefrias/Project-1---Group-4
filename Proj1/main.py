from services.libmanager import LibraryManager
from services.playlistmanager import PlaylistManager
from models.track import Track
from services.queuemanager import QueueManager
from utils.pagination import paginate
from data_struc.queueDS import MusicQueue
import json



library = LibraryManager("data/library.json")
playlist = PlaylistManager("data/playlist.json")
queue = QueueManager("data/queue_state.json")


# ========== MENUS ==========
def main_menu(): 
    print("\n1 ----> LIBRARY")
    print("2 ----> PLAYLIST")
    print("3 ----> QUEUE")
    print("4 ----> EXIT")

def libmenu():
    print("\n0 ----> Play Music")
    print("1 ----> View Music Library")
    print("2 ----> Add track")
    print("3 ----> Remove track")
    print("4 ----> Back")

def playlistmenu():
    print("\n0 ----> Play Playlist")
    print("1 ----> Create Playlist")
    print("2 ----> Delete Playlist")
    print("3 ----> Edit Playlist")
    print("4 ----> View All Playlists")
    print("5 ----> Back")

def editplmenu():
    print("\n1 ----> Rename Playlist") 
    print("2 ----> Add Track to Playlist")
    print("3 ----> Delete Track from Playlist")
    print("4 ----> Back")

# def queuemenu():
#     print("\n--- QUEUE MENU ---")
#     print("1. Add track to queue (library/manual)")
#     print("2. Show queue")
#     print("3. Play current track")
#     print("4. Next track")
#     print("5. Previous track")
#     print("6. Remove a track from queue")
#     print("7. Back to main menu")

def queuemenu():
    print("1 ----> Play")
    print("2 ----> Next")
    print("3 ----> Previous")
    print("4 ----> Toggle Repeat")
    print("5 ----> Toggle Shuffle")
    print("6 ----> Clear Queue")
    print("7 ----> Back")

def display_queue_interface(queue):
    """Display queue info in interface format like the example."""
    if queue.get_size() == 0:
        print("Queue is empty.")
        return

    # Header: Duration, shuffle, repeat
    print(f"Total Duration: {queue.get_total_duration()}")
    print(f"Shuffled: {'Yes' if queue.is_shuffled() else 'No'}")
    print(f"Repeat: {'Yes' if queue.is_repeat_on() else 'No'}")
    print("Tracks:\n")

    # Current track
    current = queue.get_current_track()
    status = "Paused" if queue.is_playing() == False else "Playing"
    if current:
        print(f"Currently {status}:")
        print(f"\n{current.title} – {current.artist} ({current.duration})\n")

    # Next tracks (up to 10 items)
    print("Next:")
    current_idx = queue._MusicQueue__current_index if hasattr(queue, '_MusicQueue__current_index') else 0
    tracks = queue.get_tracks()
    max_show = min(10, len(tracks) - current_idx - 1)
    
    if max_show <= 0:
        print("(No more tracks)")
    else:
        for i in range(1, max_show + 1):
            next_idx = current_idx + i
            if next_idx < len(tracks):
                t = tracks[next_idx]
                print(f"({i})\t{t.title} – {t.artist} ({t.duration})")
    
    print("\n" + "="*60 + "\n")

#MAIN LOOP
while True:
    main_menu()
    choice = input("Choose: ")

    # LIBRARY 
    if choice == "1":
        while True:
            libmenu()
            choice2 = input("Choose: ")

            # PLAY MUSIC (PAGINATED)
            if choice2 == "0":
                page = 1
                tracks = library.tracks.to_list()

                while True:
                    paginate(tracks, page=page, page_size=10, title="LIBRARY TRACKS")
                    cmd = input("Choose: ").lower().strip()

                    if cmd == "n":
                        if page * 10 < len(tracks):
                            page += 1
                        else:
                            print("Last page.")

                    elif cmd == "p":
                        if page > 1:
                            page -= 1
                        else:
                            print("First page.")

                    elif cmd == "b":
                        break

                    elif cmd.isdigit():
                        index = int(cmd) - 1
                        library.play(index)

                        while True:
                            print("\nPlay <p>  \nStop <s> \nNext <n> \nPrevious <pr> \nBack <b>")
                            action = input("Choose: ").lower()

                            if action == "p":
                                library.play(library.current_index)
                            elif action == "s":
                                library.stop()
                            elif action == "n":
                                library.next()
                            elif action == "pr":
                                library.previous()
                            elif action == "b":
                                break
                            else:
                                print("Invalid option")
                    else:
                        print("Invalid option.")

            #  VIEW LIBRARY (PAGINATED)
            elif choice2 == "1":
                page = 1
                tracks = library.tracks.to_list()

                while True:
                    paginate(tracks, page=page, page_size=10, title="LIBRARY TRACKS")
                    cmd = input("Choose: ").lower().strip()

                    if cmd == "n":
                        if page * 10 < len(tracks):
                            page += 1
                        else:
                            print("Last page.")

                    elif cmd == "p":
                        if page > 1:
                            page -= 1
                        else:
                            print("First page.")

                    elif cmd == "b":
                        break

            elif choice2 == "2":
                title = input("Title: ")
                artist = input("Artist: ")
                album = input("Album: ")
                duration = input("Duration (mm:ss): ")
                library.add(Track(title, artist, album, duration))
                print("Track added successfully!")

            elif choice2 == "3":
                index = int(input("Track number to delete: ")) - 1
                library.delete(index)

            elif choice2 == "4":
                break
            else:
                print("Invalid option")


    # PLAYLIST
    elif choice == "2":
        while True:
            playlistmenu()
            choice2 = input("Choose: ")

            # PLAY PLAYLIST (PAGINATED)
            if choice2 == "0":
                name = input("Playlist name: ")
                playlist.open_playlist(name)
                tracks = playlist.tracks
                page = 1

                while True:
                    paginate(tracks.to_list(), page=page, page_size=10, title=f"PLAYLIST: {name}")
                    cmd = input("Choose: ").lower().strip()

                    if cmd == "n":
                        if page * 10 < len(tracks):
                            page += 1
                        else:
                            print("Last page.")

                    elif cmd == "p":
                        if page > 1:
                            page -= 1
                        else:
                            print("First page.")

                    elif cmd == "b":
                        break

                    elif cmd.isdigit():
                        index = int(cmd) - 1
                        playlist.play(index)

                        while True:
                            print("\nPlay <p> | Stop <s> | Next <n> | Previous <pr> | Back <b>")
                            action = input("Choose: ").lower()

                            if action == "p":
                                playlist.play(playlist.current_index)
                            elif action == "s":
                                playlist.stop()
                            elif action == "n":
                                playlist.next()
                            elif action == "pr":
                                playlist.previous()
                            elif action == "b":
                                break
                            else:
                                print("Invalid option")

            elif choice2 == "1":
                name = input("New playlist name: ")
                playlist.create_playlist(name)

            elif choice2 == "2":
                name = input("Playlist to delete: ")
                playlist.delete_playlist(name)

            elif choice2 == "3":
                name = input("Playlist to edit: ")
                playlist.open_playlist(name)

                while True:
                    editplmenu()
                    action = input("Choose: ")

                    if action == "1":
                        new_name = input("New name: ")
                        playlist.rename_playlist(name, new_name)
                        name = new_name

                    elif action == "2":
                        title = input("Title: ")
                        artist = input("Artist: ")
                        album = input("Album: ")
                        duration = input("Duration: ")
                        playlist.add_track(Track(title, artist, album, duration))

                    elif action == "3":
                        tracks = playlist.tracks
                        page = 1

                        while True:
                            paginate(tracks, page=page, page_size=10, title=f"EDIT: {name}")
                            cmd = input("Choose: ").lower().strip()

                            if cmd == "n":
                                if page * 10 < len(tracks):
                                    page += 1
                                else:
                                    print("Last page.")

                            elif cmd == "p":
                                if page > 1:
                                    page -= 1
                                else:
                                    print("First page.")

                            elif cmd == "b":
                                break

                            elif cmd.isdigit():
                                playlist.delete_track(int(cmd) - 1)
                                break

                    elif action == "4":
                        break

                    else:
                        print("Invalid option")

            elif choice2 == "4":
                page = 1

                with open("data/playlist.json", "r") as file:
                    data = json.load(file)
                    item = data["playlists"]

                while True:
                    paginate(item, page=page, page_size=10, title="PLAYLISTS")

                    cmd = input("Choose: ").lower().strip()

                    if cmd == "n":
                        if page * 10 < len(item):
                            page += 1
                        else:
                            print("Last page.")

                    elif cmd == "p":
                        if page > 1:
                            page -= 1
                        else:
                            print("First page.")

                    elif cmd == "b":
                        break

                    else:
                        print("Invalid option")
            elif choice2 == "5":
                break
            else:
                print("Invalid Choice")

    # ===== QUEUE =====
    elif choice == "3":
        while True:
            queuemenu()
            q_choice = input("Choose: ").strip()

            if q_choice == "1":
                # Add track from library or manually
                queue.add_to_queue_from_library_or_manual(library)
                queue.queue.save_state()  # persist immediately

            elif q_choice == "2":
                # Show queue
                display_queue_interface(queue)

            elif q_choice == "3":
                # Play current track
                queue.queue.play()
                current = queue.queue.get_current_track()
                if current:
                    print(f"Now Playing: {current.title} – {current.artist} ({current.duration})")
                else:
                    print("Queue is empty.")

            elif q_choice == "4":
                # Next track
                next_track = queue.queue.next_track()
                if next_track:
                    print(f"Now Playing: {next_track.title} – {next_track.artist} ({next_track.duration})")
                else:
                    print("Reached end of queue.")
                queue.queue.save_state()

            elif q_choice == "5":
                # Previous track
                prev_track = queue.queue.previous_track()
                if prev_track:
                    print(f"Now Playing: {prev_track.title} – {prev_track.artist} ({prev_track.duration})")
                else:
                    print("Reached start of queue.")
                queue.queue.save_state()

            elif q_choice == "6":
                # Remove a track
                if queue.queue.get_size() == 0:
                    print("Queue is empty.")
                    continue
                display_queue_interface(queue)
                try:
                    index = int(input("Enter track number to remove: ")) - 1
                    removed = queue.queue.get_tracks()[index]
                    queue.queue._MusicQueue__tracks.remove(index)  # directly remove from ArrayList
                    queue.queue.save_state()
                    print(f"Removed '{removed.title}' from the queue.")
                except (IndexError, ValueError):
                    print("Invalid track number.")

            elif q_choice == "7":
                break

            elif q_choice.lower() == "s":
                # Optional: toggle shuffle
                queue.queue.shuffle()
                print(f"Shuffle is now {'ON' if queue.queue.is_shuffled() else 'OFF'}")
                queue.queue.save_state()

            elif q_choice.lower() == "r":
                # Optional: toggle repeat
                repeat_state = queue.queue.toggle_repeat()
                print(f"Repeat is now {'ON' if repeat_state else 'OFF'}")
                queue.queue.save_state()

            else:
                print("Invalid option.")


    # # ===== QUEUE =====
    # elif choice == "3":
    #     while True:
    #         queuemenu()
    #         q_choice = input("Choose: ").strip()

    #         if q_choice == "1":
    #             # page = 1
    #             # tracks = queue.queue.to_list()
    #             # paginate(tracks, page=page, page_size=10, title="QUEUE")
    #             queue.add_to_queue_from_library_or_manual(library)
    #             # paginate(tracks, page=page, page_size=10, title="QUEUE")

    #         # SHOW QUEUE (PAGINATED)
    #         elif q_choice == "2":  # Show queue
    #             if queue.queue.length() == 0:  # optional check
    #                 print("Queue is empty.")
    #                 continue

    #             page = 1
    #             while True:
    #                 #  Convert ArrayList to list first
    #                 tracks = queue.queue.to_list()
    #                 paginate(tracks, page=page, page_size=10, title="QUEUE TRACKS")

    #                 cmd = input("Next (n) | Prev (p) | Back (b): ").lower().strip()

    #                 if cmd == "n":
    #                     if page * 10 < len(tracks):
    #                         page += 1
    #                     else:
    #                         print("Last page.")
    #                 elif cmd == "p":
    #                     if page > 1:
    #                         page -= 1
    #                     else:
    #                         print("First page.")
    #                 elif cmd == "b":
    #                     break
    #                 else:
    #                     print("Invalid option")

    #         elif q_choice == "3":
    #             queue.play_current()

    #         elif q_choice == "4":
    #             queue.next_track()

    #         elif q_choice == "5":
    #             queue.previous_track()

    #         elif q_choice == "6":
    #             queue.remove_track()

    #         elif q_choice == "7":
    #             break

    #         else:
    #             print("Invalid option.")


    # EXIT
    elif choice == "4":
        print("Exiting...")
        break

    else:
        print("Invalid option")
