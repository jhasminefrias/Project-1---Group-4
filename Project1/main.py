from services.libmanager import LibraryManager
from models.track import Track


library = LibraryManager("data/library.json")


while True:
    print("1. Add Track")
    print("2. Display Library")
    print("3. Exit")


    choice = input("Choose: ")


    if choice == "1":
        title = input("Title: ")
        artist = input("Artist: ")
        album = input("Album: ")
        duration = input("Duration (mm:ss): ")


        track = Track(title, artist, album, duration)
        library.add(track)
        print("Track added successfully!")

    elif choice == "2":
        library.display_tracks()

    elif choice == "3":
        break

    else:
        print("Invalid option")