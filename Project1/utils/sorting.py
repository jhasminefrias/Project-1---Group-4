def bubble_sort(tracks):
    n = len(tracks)
    i = 0
    while i < n:
        j = 0
        while j < n - i - 1:
            if tracks[j]["title"].lower() > tracks[j + 1]["title"].lower():
                temp = tracks[j]
                tracks[j] = tracks[j + 1]
                tracks[j + 1] = temp
            j += 1
        i += 1
    return tracks