from services.libmanager import LibraryManager
from services.playlistmanager import PlaylistManager
from models.track import Track


library = LibraryManager("data/library.json")
playlist = PlaylistManager("data/playlist.json")

def main_menu(): 
    print ("1 ----> LIBRARY")
    print ("2 ----> PLAYLIST")
    print ("3 ----> QUEUE")
    print ("4 ----> EXIT")

def libmenu():
    print ("0 ----> Play Music")
    print ("1 ----> Enqueue Library to Queue")
    # print ("2 ----> Play Library")
    print ("3 ----> View Music Library")
    print ("4 ----> Add track")
    print ("5 ----> Remove track")
    print ("6 ----> Add Track to Queue")
    print ("7 ----> Back")

def playlistmenu():
    print ("0 ----> Play Playlist")
    print ("1 ----> Create Playlist")
    print ("2 ----> Delete Playlist")
    print ("3 ----> Edit Playlist")
    print ("4 ----> Exit")


while True:
    main_menu()
    choice = input("Choose: ")

    if choice == "1":
        libmenu()
        choice2 = input("Choose: ")

        if choice2 == "0":
            library.display_tracks()
            option = int(input("Input the number you want to play: ")) - 1
            print (f"Currently Playing: {library.get_track(option)}")

            print ("Play <p>")
            print ("Stop <s>")
            print ("Next <n>")
            print ("Previous <pr>")
            option1 = input("Choose: ")

            if option1 == "p":
                library.play(option)
            elif option1 == "s":
                library.stop()
            elif option1 == "n":
                library.next()
            elif option1 == "pr":
                library.previous()


        elif choice2 == "4":
            title = input("Title: ")
            artist = input("Artist: ")
            album = input("Album: ")
            duration = input("Duration (mm:ss): ")


            track = Track(title, artist, album, duration)
            library.add(track)
            print("Track added successfully!")

        elif choice2 == "3":
            library.display_tracks()
        
        elif choice2 == "5":
            index = int(input("Enter the number of the track you want to delete: ")) - 1
            library.delete(index)

        elif choice2 == "3":
            break

        else:
            print("Invalid option")
    elif choice == "2":
        playlistmenu()
        choice2 = input("Choose: ")

        if choice2 == "0":
            pass
        elif choice2 == "1":
            name = input("Enter Name: ")
            playlist.create_playlist(name)

            print ("Yes (Y) \nNo(N)")
            print ("Do you want to add track?: ")
            option1 = input("Choose: ")

            if option1 == "Y":
                title = input("Title: ")
                artist = input("Artist: ")
                album = input("Album: ")
                duration = input("Duration (mm:ss): ")


                track = Track(title, artist, album, duration)
                playlist.add_track(track)
