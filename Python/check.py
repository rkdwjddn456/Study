import os
import json

floder_path = r"C:/Users/Administrator/Desktop/python/json_2"

with open("./error_2.txt", 'w', encoding='utf8') as error_f:
    for root, dirs, files in os.walk(floder_path):
        for file in files:
            if file.split(".")[-1].lower() == "json":
                with open(root + "/" + file, 'r', encoding='utf8') as json_f:
                    json_data = json.load(json_f)

                    annotations = json_data["annotations"]
                    class_no = file.split("_")[1]

                    for anotation in annotations:
                        if str(anotation["object_id"]) != class_no:
                            print(file)
                            error_f.write(file + "\n")
                            break