import os
import json
from operator import itemgetter

def statistics():
    person_count = {
        'male' : 0,
        'female' : 0,
        'child' : 0,
        'teenager' : 0,
        'adult' : 0,
        'senior' : 0,
        'long_sleeve' : 0,
        'short_sleeve' : 0,
        'sleeveless' : 0,
        'onepice' : 0,
        'top_red' : 0,
        'top_orange' : 0,
        'top_yellow' : 0,
        'top_green' : 0,
        'top_blue' : 0,
        'top_purple' : 0,
        'top_pink' : 0,
        'top_brown' : 0,
        'top_white' : 0,
        'top_grey' : 0,
        'top_black' : 0,
        'long_pants' : 0,
        'short_pants' : 0,
        'skirt' : 0,
        'bottom_type_none' : 0,
        'bottom_red' : 0,
        'bottom_orange' : 0,
        'bottom_yellow' : 0,
        'bottom_green' : 0,
        'bottom_blue' : 0,
        'bottom_purple' : 0,
        'bottom_pink' : 0,
        'bottom_brown' : 0,
        'bottom_white' : 0,
        'bottom_grey' : 0,
        'bottom_black' : 0,
        'bottom_color_none' : 0,
        'carrier' : 0,
        'umbrella' : 0,
        'bag' : 0,
        'hat' : 0,
        'glasses' : 0,
        'acc_none' : 0,
        'pet' : 0
    }

    filtering_folder = []
    tb = ["2021-08-05_09-21-00_thu_sunny_out_ju-ja_c0241.json","2021-08-05_09-24-00_thu_sunny_out_ju-ja_c0241.json","2021-08-05_09-27-00_thu_sunny_out_ju-ja_c0241.json",
          "2021-08-05_09-33-00_thu_sunny_out_ju-ja_c0241.json","2021-08-05_09-36-00_thu_sunny_out_ju-ja_c0241.json","2021-08-05_09-39-00_thu_sunny_out_ju-ja_c0241.json",
          "2021-08-05_10-00-00_thu_sunny_out_ju-ja_c0241.json","2021-08-06_12-24-00_fri_sunny_out_ju-ja_c0241.json","2021-08-06_12-27-00_fri_sunny_out_ju-ja_c0241.json",
          "2021-08-08_08-18-00_sun_sunny_out_ju-ja_c0065.json","2021-08-08_08-33-00_sun_sunny_out_ju-ja_c0065.json","2021-08-08_08-45-00_sun_sunny_out_ju-ja_c0065.json",
          "2021-08-08_10-09-00_sun_sunny_out_ju-ja_c0241.json","2021-08-08_11-36-00_sun_sunny_out_ju-ja_c0241.json","2021-08-09_08-51-00_mon_sunny_out_ju-ja_c0063.json",
          "2021-08-10_08-21-00_tue_sunny_out_ju-ja_c0071.json","2021-08-10_08-24-00_tue_sunny_out_ju-ja_c0071.json","2021-08-10_08-27-00_tue_sunny_out_ju-ja_c0071.json",
          "2021-08-10_08-36-00_tue_sunny_out_ju-ja_c0065.json","2021-08-10_08-51-00_tue_sunny_out_ju-ja_c0065.json","2021-08-10_10-06-00_tue_sunny_out_ju-ja_c0241.json",
          "2021-08-10_10-09-00_tue_sunny_out_ju-ja_c0241.json","2021-08-10_10-12-00_tue_sunny_out_ju-ja_c0241.json","2021-08-10_10-15-00_tue_sunny_out_ju-ja_c0241.json",
          "2021-08-10_10-42-00_tue_sunny_out_ju-ja_c0241.json","2021-08-10_10-45-00_tue_sunny_out_ju-ja_c0241.json"]

    floder_path = r"C:\Users\Administrator\Desktop\label\label_test"
    # floder_path = input("경로를 입력하세요: ")

    for root, dirs, files in os.walk(floder_path):
        dirs[:] = [dir for dir in dirs if dir.lower() not in filtering_folder]
        for file in files:
            if file in tb:
                continue
            file_name, extension = os.path.splitext(file)
            if extension == ".json":
                print(file)
                with open(root + "/" + file, 'r', encoding='utf8') as json_f:
                    json_data = json.load(json_f)

                    categories = json_data["categories"]

                    annotations = json_data["annotations"]
                    sort_annotations = sorted(annotations, key=itemgetter("frame"))
                    process_annotations = []
                    for annotation in sort_annotations:
                        if annotation["id"][0] == "p" or annotation["id"][0] == "a":
                            annotation["gender"] = [category["gender"] for category in categories if category["id"] == annotation["id"]][0]                           
                            annotation["age"] = [category["age"] for category in categories if category["id"] == annotation["id"]][0]
                            process_annotations.append(annotation)
                
                for process_annotation in process_annotations:
                    person_count[process_annotation["gender"]] += 1
                    person_count[process_annotation["age"]] += 1
                    person_count[process_annotation["top_type"]] += 1
                    person_count["top_" + process_annotation["top_color"]] += 1

                    bottom_type = process_annotation["bottom_type"]
                    if bottom_type == "none" :
                        person_count["bottom_type_none"] += 1
                    else:
                        person_count[process_annotation["bottom_type"]] += 1

                    bottom_color = process_annotation["bottom_color"]
                    if bottom_color == "none":
                        person_count["bottom_color_none"] += 1
                    else:
                        person_count["bottom_" + process_annotation["bottom_color"]] += 1

                    accessories = process_annotation["accessories"]
                    if accessories == "none":
                        person_count["acc_none"] += 1
                    else:
                        person_count[process_annotation["accessories"]] += 1

                    person_count["pet"] += process_annotation["pet"]

    print(person_count)
    print("==========================Done==========================")
    while True:
        pass

try:
    statistics()
except Exception as e:
    print(e)
    while(True):
        continue

