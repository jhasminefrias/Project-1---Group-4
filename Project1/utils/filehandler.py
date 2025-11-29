import json


def read_json(path):
    f = open(path, "r")
    data = json.load(f)
    f.close()
    return data




def write_json(path, data):
    f = open(path, "w")
    json.dump(data, f, indent=4)
    f.close()