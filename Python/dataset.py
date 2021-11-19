import cv2
import os
import json
from operator import itemgetter
from math import floor

path = r"C:\Users\Administrator\Desktop\video_test"
crop_path = r"C:\Users\Administrator\Desktop\video_test\crop_image_test"

count = 0
num_list = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
file_list = []

with open("./dataset.txt", 'w', encoding='utf8') as dataset:
    for (root, dirs, files) in os.walk(path):
        for file in files:
            file_name, ext = os.path.splitext(file)
            if ext == ".mp4":
                print("mp4 들어옴 ", file_name)
                vidcap = cv2.VideoCapture(file)
                success, image = vidcap.read()
                while success:               
                    cv2.imwrite(path + "\\image_test\\frame%d.jpg" %count , image) # memory에 있는걸 hard disk에 다시 쓰는거라서 없어도 됨
                    success, image = vidcap.read()
                    count += 1

                    if success == False:           
                        with open(root + "/" + file_name + ".json" , encoding="utf-8") as json_file:               
                            print("json 들어옴 ", file_name)
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
                    
                            for i in range(len(process_annotations)):
                                x_1 = process_annotations[i]["bbox"][1]
                                x_2 = process_annotations[i]["bbox"][3]
                                y_1 = process_annotations[i]["bbox"][0]
                                y_2 = process_annotations[i]["bbox"][2]

                                img = cv2.imread(path + "\\image_test\\frame%d.jpg"%process_annotations[i]["frame"]) # memory에 있는걸 굳이 안불러와도 됨       
                                cropped_img = img[int(x_1):int(x_2), int(y_1):int(y_2)]

                                cv2.imwrite(crop_path + "\\" + file_name + '_' + process_annotations[0]["id"] + '_'+ "%d.jpg" %i , cropped_img)

                                if process_annotations[i]["gender"] == "male":
                                    num_list[0] = 1
                                    num_list[1] = 0
                                elif process_annotations[i]["gender"] == "female":
                                    num_list[0] = 0
                                    num_list[1] = 1 

                                if process_annotations[i]["age"] == "child":
                                    num_list[2] = 1
                                    num_list[3] = 0
                                    num_list[4] = 0
                                    num_list[5] = 0
                                elif process_annotations[i]["age"] == "teenager":
                                    num_list[2] = 0
                                    num_list[3] = 1
                                    num_list[4] = 0
                                    num_list[5] = 0
                                elif process_annotations[i]["age"] == "adult":
                                    num_list[2] = 0
                                    num_list[3] = 0
                                    num_list[4] = 1
                                    num_list[5] = 0
                                elif process_annotations[i]["age"] == "senior":
                                    num_list[2] = 0
                                    num_list[3] = 0
                                    num_list[4] = 0
                                    num_list[5] = 1

                                if process_annotations[i]["top_type"] == "long_sleeve":
                                    num_list[6] = 1
                                    num_list[7] = 0
                                    num_list[8] = 0
                                    num_list[9] = 0
                                elif process_annotations[i]["top_type"] == "short_sleeve":
                                    num_list[6] = 0
                                    num_list[7] = 1
                                    num_list[8] = 0
                                    num_list[9] = 0
                                elif process_annotations[i]["top_type"] == "sleeveless":
                                    num_list[6] = 0
                                    num_list[7] = 0
                                    num_list[8] = 1
                                    num_list[9] = 0
                                elif process_annotations[i]["top_type"] == "onepice":
                                    num_list[6] = 0
                                    num_list[7] = 0
                                    num_list[8] = 0
                                    num_list[9] = 1
                                    
                                if process_annotations[i]["top_color"] == "red":
                                    num_list[10] = 1
                                    num_list[11] = 0
                                    num_list[12] = 0
                                    num_list[13] = 0
                                    num_list[14] = 0
                                    num_list[15] = 0
                                    num_list[16] = 0
                                    num_list[17] = 0
                                    num_list[18] = 0
                                    num_list[19] = 0
                                    num_list[20] = 0
                                elif process_annotations[i]["top_color"] == "orange":
                                    num_list[10] = 0
                                    num_list[11] = 1
                                    num_list[12] = 0
                                    num_list[13] = 0
                                    num_list[14] = 0
                                    num_list[15] = 0
                                    num_list[16] = 0
                                    num_list[17] = 0
                                    num_list[18] = 0
                                    num_list[19] = 0
                                    num_list[20] = 0
                                elif process_annotations[i]["top_color"] == "yellow":
                                    num_list[10] = 0
                                    num_list[11] = 0
                                    num_list[12] = 1
                                    num_list[13] = 0
                                    num_list[14] = 0
                                    num_list[15] = 0
                                    num_list[16] = 0
                                    num_list[17] = 0
                                    num_list[18] = 0
                                    num_list[19] = 0
                                    num_list[20] = 0
                                elif process_annotations[i]["top_color"] == "green":
                                    num_list[10] = 0
                                    num_list[11] = 0
                                    num_list[12] = 0
                                    num_list[13] = 1
                                    num_list[14] = 0
                                    num_list[15] = 0
                                    num_list[16] = 0
                                    num_list[17] = 0
                                    num_list[18] = 0
                                    num_list[19] = 0
                                    num_list[20] = 0
                                elif process_annotations[i]["top_color"] == "blue":
                                    num_list[10] = 0
                                    num_list[11] = 0
                                    num_list[12] = 0
                                    num_list[13] = 0
                                    num_list[14] = 1
                                    num_list[15] = 0
                                    num_list[16] = 0
                                    num_list[17] = 0
                                    num_list[18] = 0
                                    num_list[19] = 0
                                    num_list[20] = 0
                                elif process_annotations[i]["top_color"] == "purple":
                                    num_list[10] = 0
                                    num_list[11] = 0
                                    num_list[12] = 0
                                    num_list[13] = 0
                                    num_list[14] = 0
                                    num_list[15] = 1
                                    num_list[16] = 0
                                    num_list[17] = 0
                                    num_list[18] = 0
                                    num_list[19] = 0
                                    num_list[20] = 0
                                elif process_annotations[i]["top_color"] == "pink":
                                    num_list[10] = 0
                                    num_list[11] = 0
                                    num_list[12] = 0
                                    num_list[13] = 0
                                    num_list[14] = 0
                                    num_list[15] = 0
                                    num_list[16] = 1
                                    num_list[17] = 0
                                    num_list[18] = 0
                                    num_list[19] = 0
                                    num_list[20] = 0
                                elif process_annotations[i]["top_color"] == "brown":
                                    num_list[10] = 0
                                    num_list[11] = 0
                                    num_list[12] = 0
                                    num_list[13] = 0
                                    num_list[14] = 0
                                    num_list[15] = 0
                                    num_list[16] = 0
                                    num_list[17] = 1
                                    num_list[18] = 0
                                    num_list[19] = 0
                                    num_list[20] = 0
                                elif process_annotations[i]["top_color"] == "white":
                                    num_list[10] = 0
                                    num_list[11] = 0
                                    num_list[12] = 0
                                    num_list[13] = 0
                                    num_list[14] = 0
                                    num_list[15] = 0
                                    num_list[16] = 0
                                    num_list[17] = 0
                                    num_list[18] = 1
                                    num_list[19] = 0
                                    num_list[20] = 0
                                elif process_annotations[i]["top_color"] == "grey":
                                    num_list[10] = 0
                                    num_list[11] = 0
                                    num_list[12] = 0
                                    num_list[13] = 0
                                    num_list[14] = 0
                                    num_list[15] = 0
                                    num_list[16] = 0
                                    num_list[17] = 0
                                    num_list[18] = 0
                                    num_list[19] = 1
                                    num_list[20] = 0
                                elif process_annotations[i]["top_color"] == "black":
                                    num_list[10] = 0
                                    num_list[11] = 0
                                    num_list[12] = 0
                                    num_list[13] = 0
                                    num_list[14] = 0
                                    num_list[15] = 0
                                    num_list[16] = 0
                                    num_list[17] = 0
                                    num_list[18] = 0
                                    num_list[19] = 0
                                    num_list[20] = 1
                                
                                if process_annotations[i]["bottom_type"] == "long_pants":
                                    num_list[21] = 1
                                    num_list[22] = 0
                                    num_list[23] = 0
                                    num_list[24] = 0
                                elif process_annotations[i]["bottom_type"] == "short_pants":
                                    num_list[21] = 0
                                    num_list[22] = 1
                                    num_list[23] = 0
                                    num_list[24] = 0
                                elif process_annotations[i]["bottom_type"] == "skirt":
                                    num_list[21] = 0
                                    num_list[22] = 0
                                    num_list[23] = 1
                                    num_list[24] = 0
                                elif process_annotations[i]["bottom_type"] == "none":
                                    num_list[21] = 0
                                    num_list[22] = 0
                                    num_list[23] = 0
                                    num_list[24] = 1

                                if process_annotations[i]["bottom_color"] == "red":
                                    num_list[25] = 1
                                    num_list[26] = 0
                                    num_list[27] = 0
                                    num_list[28] = 0
                                    num_list[29] = 0
                                    num_list[30] = 0
                                    num_list[31] = 0
                                    num_list[32] = 0
                                    num_list[33] = 0
                                    num_list[34] = 0
                                    num_list[35] = 0
                                elif process_annotations[i]["bottom_color"] == "orange":
                                    num_list[25] = 0
                                    num_list[26] = 1
                                    num_list[27] = 0
                                    num_list[28] = 0
                                    num_list[29] = 0
                                    num_list[30] = 0
                                    num_list[31] = 0
                                    num_list[32] = 0
                                    num_list[33] = 0
                                    num_list[34] = 0
                                    num_list[35] = 0
                                elif process_annotations[i]["bottom_color"] == "yellow":
                                    num_list[25] = 0
                                    num_list[26] = 0
                                    num_list[27] = 1
                                    num_list[28] = 0
                                    num_list[29] = 0
                                    num_list[30] = 0
                                    num_list[31] = 0
                                    num_list[32] = 0
                                    num_list[33] = 0
                                    num_list[34] = 0
                                    num_list[35] = 0
                                elif process_annotations[i]["bottom_color"] == "green":
                                    num_list[25] = 0
                                    num_list[26] = 0
                                    num_list[27] = 0
                                    num_list[28] = 1
                                    num_list[29] = 0
                                    num_list[30] = 0
                                    num_list[31] = 0
                                    num_list[32] = 0
                                    num_list[33] = 0
                                    num_list[34] = 0
                                    num_list[35] = 0
                                elif process_annotations[i]["bottom_color"] == "blue":
                                    num_list[25] = 0
                                    num_list[26] = 0
                                    num_list[27] = 0
                                    num_list[28] = 0
                                    num_list[29] = 1
                                    num_list[30] = 0
                                    num_list[31] = 0
                                    num_list[32] = 0
                                    num_list[33] = 0
                                    num_list[34] = 0
                                    num_list[35] = 0
                                elif process_annotations[i]["bottom_color"] == "purple":
                                    num_list[25] = 0
                                    num_list[26] = 0
                                    num_list[27] = 0
                                    num_list[28] = 0
                                    num_list[29] = 0
                                    num_list[30] = 1
                                    num_list[31] = 0
                                    num_list[32] = 0
                                    num_list[33] = 0
                                    num_list[34] = 0
                                    num_list[35] = 0
                                elif process_annotations[i]["bottom_color"] == "pink":
                                    num_list[25] = 0
                                    num_list[26] = 0
                                    num_list[27] = 0
                                    num_list[28] = 0
                                    num_list[29] = 0
                                    num_list[30] = 0
                                    num_list[31] = 1
                                    num_list[32] = 0
                                    num_list[33] = 0
                                    num_list[34] = 0
                                    num_list[35] = 0
                                elif process_annotations[i]["bottom_color"] == "brown":
                                    num_list[25] = 0
                                    num_list[26] = 0
                                    num_list[27] = 0
                                    num_list[28] = 0
                                    num_list[29] = 0
                                    num_list[30] = 0
                                    num_list[31] = 0
                                    num_list[32] = 1
                                    num_list[33] = 0
                                    num_list[34] = 0
                                    num_list[35] = 0
                                elif process_annotations[i]["bottom_color"] == "white":
                                    num_list[25] = 0
                                    num_list[26] = 0
                                    num_list[27] = 0
                                    num_list[28] = 0
                                    num_list[29] = 0
                                    num_list[30] = 0
                                    num_list[31] = 0
                                    num_list[32] = 0
                                    num_list[33] = 1
                                    num_list[34] = 0
                                    num_list[35] = 0
                                elif process_annotations[i]["bottom_color"] == "grey":
                                    num_list[25] = 0
                                    num_list[26] = 0
                                    num_list[27] = 0
                                    num_list[28] = 0
                                    num_list[29] = 0
                                    num_list[30] = 0
                                    num_list[31] = 0
                                    num_list[32] = 0
                                    num_list[33] = 0
                                    num_list[34] = 1
                                    num_list[35] = 0
                                elif process_annotations[i]["bottom_color"] == "black":
                                    num_list[25] = 0
                                    num_list[26] = 0
                                    num_list[27] = 0
                                    num_list[28] = 0
                                    num_list[29] = 0
                                    num_list[30] = 0
                                    num_list[31] = 0
                                    num_list[32] = 0
                                    num_list[33] = 0
                                    num_list[34] = 0
                                    num_list[35] = 1
                                
                                if process_annotations[i]["accessories"] == "carrier":
                                    num_list[36] = 1
                                    num_list[37] = 0
                                    num_list[38] = 0
                                    num_list[39] = 0
                                    num_list[40] = 0
                                    num_list[41] = 0
                                elif process_annotations[i]["accessories"] == "umbrella":
                                    num_list[36] = 0
                                    num_list[37] = 1
                                    num_list[38] = 0
                                    num_list[39] = 0
                                    num_list[40] = 0
                                    num_list[41] = 0
                                elif process_annotations[i]["accessories"] == "bag":
                                    num_list[36] = 0
                                    num_list[37] = 0
                                    num_list[38] = 1
                                    num_list[39] = 0
                                    num_list[40] = 0
                                    num_list[41] = 0
                                elif process_annotations[i]["accessories"] == "hat":
                                    num_list[36] = 0
                                    num_list[37] = 0
                                    num_list[38] = 0
                                    num_list[39] = 1
                                    num_list[40] = 0
                                    num_list[41] = 0
                                elif process_annotations[i]["accessories"] == "glasses":
                                    num_list[36] = 0
                                    num_list[37] = 0
                                    num_list[38] = 0
                                    num_list[39] = 0
                                    num_list[40] = 1
                                    num_list[41] = 0
                                elif process_annotations[i]["accessories"] == "none":
                                    num_list[36] = 0
                                    num_list[37] = 0
                                    num_list[38] = 0
                                    num_list[39] = 0
                                    num_list[40] = 0
                                    num_list[41] = 1

                                if process_annotations[i]["pet"] == 1:
                                    num_list[42] = 1
                                elif process_annotations[i]["pet"] == 0:
                                    num_list[42] = 0
                                
                                dataset.write(file_name + '_' + process_annotations[i]["id"] + '_'+ "%d.jpg" %i + ' ' + str(num_list[0]) + ' ' + str(num_list[1]) + ' ' + str(num_list[2]) + ' ' +str(num_list[3]) + ' ' + str(num_list[4]) + ' ' +str(num_list[5])+ ' ' + str(num_list[6]) + ' ' + str(num_list[7]) + ' ' + str(num_list[8]) + ' ' + str(num_list[9]) + ' ' + str(num_list[10]) + ' ' + str(num_list[11]) + ' ' +str(num_list[12]) +' ' + str(num_list[13]) + ' ' + str(num_list[14]) + ' ' +str(num_list[15]) +' ' + str(num_list[16]) + ' ' + str(num_list[17]) + ' ' +str(num_list[18]) +' ' + str(num_list[19]) + ' ' + str(num_list[20]) + ' ' +str(num_list[21]) + ' ' + str(num_list[22]) + ' ' + str(num_list[23]) + ' ' +str(num_list[24]) +' ' + str(num_list[25]) + ' ' + str(num_list[26]) + ' ' +str(num_list[27]) +' ' + str(num_list[28]) + ' ' + str(num_list[29]) + ' ' +str(num_list[30]) +' ' + str(num_list[31]) + ' ' + str(num_list[32]) + ' ' +str(num_list[33]) +' ' + str(num_list[34]) + ' ' + str(num_list[35]) + ' ' +str(num_list[36]) +' ' + str(num_list[37]) + ' ' + str(num_list[38]) + ' ' +str(num_list[39]) +' ' + str(num_list[40]) + ' ' + str(num_list[41]) + ' ' +str(num_list[42]) + '\n')

print('----- Finish !!!!!!!! -----')

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

print('----- Finish Dataset Split !!!!!!!! -----')