def minutes_to_seconds(duration):
    mins = int(duration[0:2])
    secs = int(duration[3:5])
    return mins * 60 + secs




def seconds_to_minutes(seconds):
    mins = seconds // 60
    secs = seconds % 60
    if secs < 10:
        return str(mins) + ":0" + str(secs)
    return str(mins) + ":" + str(secs)