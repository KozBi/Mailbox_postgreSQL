import json

userfile="Jsondata/Users.json"

name ="Adam"
with open(userfile, mode="r", encoding="utf-8") as read_file:
    fusers = json.load(read_file)
    if name in [user["username"] for user in fusers]:
        print("User already exists, try another name")
    else:print("User free")    