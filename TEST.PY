import json

file="Jsondata/Messages.json"

with open(file, mode="r+", encoding="utf-8") as f:
            messages_file= json.load(f)
            #check if key exist
            new={}
            if "1" in messages_file:
                    print(" user find")
            else: print("No user findx")