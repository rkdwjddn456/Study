import os
import json
import cv2
from operator import itemgetter
from math import floor

path = r"C:\Users\Administrator\Desktop\video_test"
crop_path = r"C:\Users\Administrator\Desktop\video_test\crop_image"

file_list = []

with open("./dataset.txt" , "w") as dataset:
    for (root , dirs, files) in os.walk(path):
        for file in files:
            file_name , ext = os.path.splitext(file)
            frame = 0

            if ext == '.json':
                with open(root + "/" + file_name + ".json" , encoding="utf-8") as json_file:
                    print("json 들어옴 ", file)
                    json_data = json.load(json_file)
                    annotations = json_data["annotations"]
                    categories = json_data["categories"]

                    sort_annotations = sorted(annotations, key=itemgetter("frame"))
                    process_annotations = []

                    for annotation in sort_annotations:
                        if annotation["id"][0] == "p" or annotation["id"][0] == "a":
                            annotation["gender"] = [category["gender"] for category in categories if category["id"] == annotation["id"]][0]                           
                            annotation["age"] = [category["age"] for category in categories if category["id"] == annotation["id"]][0]
                            process_annotations.append(annotation)

                print("mp4 들어옴", file_name + '.mp4')
        
                count = 0

                cap = cv2.VideoCapture(file_name + '.mp4')
                if cap.isOpened():
                    while True:
                        ret, image = cap.read()
                        if ret:
                            for i in range(count, len(process_annotations)):
                                if frame == process_annotations[i]['frame']:
                                    x_1 = process_annotations[i]["bbox"][1]
                                    x_2 = process_annotations[i]["bbox"][3]
                                    y_1 = process_annotations[i]["bbox"][0]
                                    y_2 = process_annotations[i]["bbox"][2]
            
                                    cropped_img = image[int(x_1):int(x_2), int(y_1):int(y_2)]
                                    cv2.imwrite(crop_path + "\\" + file_name + '_' + process_annotations[i]["id"] + '_'+ "%d.jpg" %i , cropped_img)

                                    gender = {"male": "1 0 ", "female": "0 1 "}.get(process_annotations[i]["gender"])
                                    age = {"child": "1 0 0 0 ", "teenager": "0 1 0 0 ", "adult": "0 0 1 0 ", "senior": "0 0 0 1 "}.get(process_annotations[i]["age"])
                                    top_type = {"long_sleeve": "1 0 0 0 ", "short_sleeve": "0 1 0 0 ", "sleeveless": "0 0 1 0 ", "onepice": "0 0 0 1 "}.get(process_annotations[i]["top_type"])
                                    top_color = {"red": "1 0 0 0 0 0 0 0 0 0 0 ", "orange": "0 1 0 0 0 0 0 0 0 0 0 ", "yellow": "0 0 1 0 0 0 0 0 0 0 0 ", "green": "0 0 0 1 0 0 0 0 0 0 0 ",
                                                    "blue": "0 0 0 0 1 0 0 0 0 0 0 ", "purple": "0 0 0 0 0 1 0 0 0 0 0 ", "pink": "0 0 0 0 0 0 1 0 0 0 0 ", "brown": "0 0 0 0 0 0 0 1 0 0 0 ",
                                                    "white": "0 0 0 0 0 0 0 0 1 0 0 ", "grey": "0 0 0 0 0 0 0 0 0 1 0 ", "black": "0 0 0 0 0 0 0 0 0 0 1 "}.get(process_annotations[i]["top_color"])
                                    bottom_type = {"long_pants": "1 0 0 0 ", "short_pants": "0 1 0 0 ", "skirt": "0 0 1 0 ", "none": "0 0 0 1 "}.get(process_annotations[i]["bottom_type"])
                                    bottom_color = {"red": "1 0 0 0 0 0 0 0 0 0 0 ", "orange": "0 1 0 0 0 0 0 0 0 0 0 ", "yellow": "0 0 1 0 0 0 0 0 0 0 0 ", "green": "0 0 0 1 0 0 0 0 0 0 0 ",
                                                    "blue": "0 0 0 0 1 0 0 0 0 0 0 ", "purple": "0 0 0 0 0 1 0 0 0 0 0 ", "pink": "0 0 0 0 0 0 1 0 0 0 0 ", "brown": "0 0 0 0 0 0 0 1 0 0 0 ",
                                                    "white": "0 0 0 0 0 0 0 0 1 0 0 ", "grey": "0 0 0 0 0 0 0 0 0 1 0 ", "black": "0 0 0 0 0 0 0 0 0 0 1 ", "none": "0 0 0 0 0 0 0 0 0 0 0 ", }.get(process_annotations[i]["bottom_color"])
                                    accessories = {"carrier": "1 0 0 0 0 0 ", "umbrella": "0 1 0 0 0 0 ", "bag": "0 0 1 0 0 0 ", "hat": "0 0 0 1 0 0 ", "glasses": "0 0 0 0 1 0 ", "none": "0 0 0 0 0 1 "}.get(process_annotations[i]["accessories"])                                               
                                    pet = str(process_annotations[i]["pet"])

                                    dataset.write(file_name + '_' + process_annotations[i]["id"] + '_'+ "%d.jpg" %i + " " + gender + age + top_type + top_color + bottom_type + bottom_color + accessories + pet + "\n")
                                    count += 1
                                
                                elif frame > process_annotations[i]['frame']:
                                    pass
                                elif frame < process_annotations[i]['frame']:
                                    break
                        else:
                            break

                        frame += 1
        
print('----- Finish Making Dataset -----')

for (root, dirs, files) in os.walk(path):
    for file in files:
        file_name, ext = os.path.splitext(file)
        if file_name == "dataset" and ext == ".txt":
            with open(root + "/" + file_name + ".txt", 'r', encoding='utf8') as test:
                for line in test:
                    file_list.append(line)

            train_index = floor(len(file_list) * 0.8)
            test_index = floor(len(file_list) * 0.1)

            training = file_list[ : train_index]
            testing = file_list[train_index : test_index + train_index]
            validationing = file_list[test_index + train_index : ]

            with open("./train.txt", 'w', encoding='utf8') as train:
                for i in range(len(training)):
                    train.write(str(training[i]))

            with open("./test.txt", 'w', encoding='utf8') as test:
                for i in range(len(testing)):
                    test.write(str(testing[i]))

            with open("./validation.txt", 'w', encoding='utf8') as validation:
                for i in range(len(validationing)):
                    validation.write(str(validationing[i]))

print('----- Finish Dataset Split -----')