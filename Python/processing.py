import cv2
import os
import json
from operator import itemgetter

def createFolder(directory):
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
    except OSError:
        print ('Error: Creating directory. ' +  directory)

createFolder("./images")

video_dir = "video"
process_annotations = []

with open("./dataset.txt", 'w') as dataset_f:
    for root, dirs, files in os.walk(video_dir):
        for file in files:
            file_name, extension = os.path.splitext(file)
            if extension == ".mp4":
                with open(root + "/" + file_name + ".json", 'r') as json_f:
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


                cap = cv2.VideoCapture(root + "/" + file)
                frame_no = 0
                checked_idx = 0
                if cap.isOpened():
                    while True:
                        ret, img = cap.read()
                        if ret:
                            split_process_annotations = process_annotations[checked_idx:]
                            for process_annotation in split_process_annotations:
                                if process_annotation["frame"] > frame_no:
                                    break
                                bbox = process_annotation["bbox"]
                                crop_img = img[int(bbox[1]):int(bbox[3]), int(bbox[0]):int(bbox[2])].copy()
                                jpg_file_name = file_name + "_" + process_annotation["id"] + "_" + str(process_annotation["frame"]) + ".jpg"
                                cv2.imwrite('images/' + jpg_file_name, crop_img)

                                gender_w = {"male": "1 0 ", "female": "0 1 "}.get(process_annotation["gender"])
                                age_w = {"child": "1 0 0 0 ", "teenager": "0 1 0 0 ", "adult": "0 0 1 0 ", "senior": "0 0 0 1 "}.get(process_annotation["age"])
                                top_type_w = {"long_sleeve": "1 0 0 0 ", "short_sleeve": "0 1 0 0 ", "sleeveless": "0 0 1 0 ", "onepice": "0 0 0 1 "}.get(process_annotation["top_type"])
                                top_color_w = {"red": "1 0 0 0 0 0 0 0 0 0 0 ", "orange": "0 1 0 0 0 0 0 0 0 0 0 ", "yellow": "0 0 1 0 0 0 0 0 0 0 0 ", "green": "0 0 0 1 0 0 0 0 0 0 0 ",
                                               "blue": "0 0 0 0 1 0 0 0 0 0 0 ", "purple": "0 0 0 0 0 1 0 0 0 0 0 ", "pink": "0 0 0 0 0 0 1 0 0 0 0 ", "brown": "0 0 0 0 0 0 0 1 0 0 0 ",
                                               "white": "0 0 0 0 0 0 0 0 1 0 0 ", "grey": "0 0 0 0 0 0 0 0 0 1 0 ", "black": "0 0 0 0 0 0 0 0 0 0 1 "}.get(process_annotation["top_color"])
                                bottom_type_w = {"long_pants": "1 0 0 0 ", "short_pants": "0 1 0 0 ", "skirt": "0 0 1 0 ", "none": "0 0 0 1 "}.get(process_annotation["bottom_type"])
                                bottom_color_w = {"red": "1 0 0 0 0 0 0 0 0 0 0 ", "orange": "0 1 0 0 0 0 0 0 0 0 0 ", "yellow": "0 0 1 0 0 0 0 0 0 0 0 ", "green": "0 0 0 1 0 0 0 0 0 0 0 ",
                                               "blue": "0 0 0 0 1 0 0 0 0 0 0 ", "purple": "0 0 0 0 0 1 0 0 0 0 0 ", "pink": "0 0 0 0 0 0 1 0 0 0 0 ", "brown": "0 0 0 0 0 0 0 1 0 0 0 ",
                                               "white": "0 0 0 0 0 0 0 0 1 0 0 ", "grey": "0 0 0 0 0 0 0 0 0 1 0 ", "black": "0 0 0 0 0 0 0 0 0 0 1 ", "none": "0 0 0 0 0 0 0 0 0 0 0 ", }.get(process_annotation["bottom_color"])
                                accessories_w = {"carrier": "1 0 0 0 0 0 ", "umbrella": "0 1 0 0 0 0 ", "bag": "0 0 1 0 0 0 ",
                                                 "hat": "0 0 0 1 0 0 ", "glasses": "0 0 0 0 1 0 ", "none": "0 0 0 0 0 1 "}.get(process_annotation["accessories"])
                                pet_w = str(process_annotation["pet"])

                                dataset_line = jpg_file_name + " " + gender_w + age_w + top_type_w + top_color_w + bottom_type_w + bottom_color_w + accessories_w + pet_w + "\n"
                                dataset_f.write(dataset_line)
                                checked_idx += 1
                            frame_no += 1
                        else:
                            break
                else:
                    print("can't open video.")
                cap.release()
                cv2.destroyAllWindows()