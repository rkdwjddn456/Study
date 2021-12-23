import os
import argparse
import subprocess
import shlex
import json
import shutil
import csv
import numpy as np
import math

video_count = {
    "smoking": 0,
    "fishing": 0,
    "trash_dump": 0,
    "wall_over": 0,
    "damage_to_facilities": 0,
    "banner_action": 0,
    "fliers_action": 0,
    "tent_setup": 0,
    "sit_down_bench": 0,
    "sit_down_floor": 0,
    "moving": 0,
    "stand": 0
}

dataset_divide_count = {
    "smoking": 0,
    "fishing": 0,
    "trash_dump": 0,
    "wall_over": 0,
    "damage_to_facilities": 0,
    "banner_action": 0,
    "fliers_action": 0,
    "tent_setup": 0
}

def convert(size, box):
    if int(size[0]) == 0:
        dw = 0
    else:
        dw = 1./int(size[0])

    if int(size[1]) == 0:
        dh = 0
    else:
        dh = 1./int(size[1])
    print(dw, dh)
    x = (int(box[0]) + int(box[1]))/2.0
    y = (int(box[2]) + int(box[3]))/2.0
    w = int(box[1]) - int(box[0])
    h = int(box[3]) - int(box[2])
    x = x * dw
    w = w * dw
    y = y * dh
    h = h * dh

    return(round(x, 4), round(y, 4), round(w, 4), round(h, 4))


def parser_init():
    parser = argparse.ArgumentParser()
    parser.add_argument('-dp', '--data_path', required=True, type=str, help='data directory path')
    parser.add_argument('-tp', '--to_data_path', required=True, type=str, help='create to dataset dir')

    args = parser.parse_args()

    data_path = args.data_path
    to_data_path = args.to_data_path
    return data_path, to_data_path


def dataset_divide(data_path, to_data_path):
    dataset_divide_file = open(to_data_path + "/dataset_divide.csv", 'w', newline='')
    dataset_divide_wr = csv.writer(dataset_divide_file)
    # smoking_file_txt = open(to_data_path + "/smoking.txt", 'w')
    # fishing_file_txt = open(to_data_path + "/fishing.txt", 'w')
    # trash_dump_file_txt = open(to_data_path + "/trash_dump.txt", 'w')
    # wall_over_file_txt = open(to_data_path + "/wall_over.txt", 'w')
    # damage_to_facilities_file_txt = open(to_data_path + "/damage_to_facilities.txt", 'w')
    # banner_action_file_txt = open(to_data_path + "/banner_action.txt", 'w')
    # fliers_action_file_txt = open(to_data_path + "/fliers_action.txt", 'w')
    # tent_setup_file_txt = open(to_data_path + "/tent_setup.txt", 'w')

    for root, dir, files in os.walk(data_path):

        for filename in files:
            filename_, ext = os.path.splitext(filename)
            print(filename)

            if ext == ".mp4":
                split_list = filename_.split("_")
                if split_list[1] == "1":
                    video_count["smoking"] += 1

                elif split_list[1] == "2":
                    video_count["fishing"] += 1
                    # fishing_file_txt.write(root + "/" + filename + "\n")

                elif split_list[1] == "3":
                    video_count["trash_dump"] += 1
                    # trash_dump_file_txt.write(root + "/" + filename + "\n")

                elif split_list[1] == "4":
                    video_count["wall_over"] += 1
                    # wall_over_file_txt.write(root + "/" + filename + "\n")

                elif split_list[1] == "5":
                    video_count["damage_to_facilities"] += 1
                    # damage_to_facilities_file_txt.write(root + "/" + filename + "\n")

                elif split_list[1] == "6":
                    video_count["banner_action"] += 1
                    # banner_action_file_txt.write(root + "/" + filename + "\n")

                elif split_list[1] == "7":
                    video_count["fliers_action"] += 1
                    # fliers_action_file_txt.write(root + "/" + filename + "\n")

                elif split_list[1] == "8":
                    video_count["tent_setup"] += 1
                    # tent_setup_file_txt.write(root + "/" + filename + "\n")

                elif split_list[1] == "30":
                    video_count["sit_down_bench"] += 1
                    # tent_setup_file_txt.write(root + "/" + filename + "\n")

                elif split_list[1] == "31":
                    video_count["sit_down_floor"] += 1
                    # tent_setup_file_txt.write(root + "/" + filename + "\n")

                elif split_list[1] == "32":
                    video_count["moving"] += 1
                    # tent_setup_file_txt.write(root + "/" + filename + "\n")

                elif split_list[1] == "33":
                    video_count["stand"] += 1
                    # tent_setup_file_txt.write(root + "/" + filename + "\n")

    print(video_count)

    train_ratio = 0.8
    val_ratio = 0.1
    test_ratio = 0.1

    smoking_train_round = math.ceil(video_count["smoking"] * train_ratio)
    smoking_val_round = round(video_count["smoking"] * val_ratio)
    smoking_test_round = round(video_count["smoking"] * test_ratio)
    print(smoking_train_round, smoking_val_round, smoking_test_round)

    fishing_train_round = round(video_count["fishing"] * train_ratio)
    fishing_val_round = round(video_count["fishing"] * val_ratio)
    fishing_test_round = round(video_count["fishing"] * test_ratio)

    trash_dump_train_round = round(video_count["trash_dump"] * train_ratio)
    trash_dump_val_round = round(video_count["trash_dump"] * val_ratio)
    fishing_test_round = round(video_count["trash_dump"] * test_ratio)

    wall_over_train_round = round(video_count["wall_over"] * train_ratio)
    wall_over_val_round = round(video_count["wall_over"] * val_ratio)
    fishing_test_round = round(video_count["wall_over"] * test_ratio)

    damage_to_facilities_train_round = round(video_count["damage_to_facilities"] * train_ratio)
    damage_to_facilities_val_round = round(video_count["damage_to_facilities"] * val_ratio)
    fishing_test_round = round(video_count["damage_to_facilities"] * test_ratio)

    banner_action_train_round = round(video_count["banner_action"] * train_ratio)
    banner_action_val_round = round(video_count["banner_action"] * val_ratio)
    fishing_test_round = round(video_count["banner_action"] * test_ratio)

    fliers_action_train_round = round(video_count["fliers_action"] * train_ratio)
    fliers_action_val_round = round(video_count["fliers_action"] * val_ratio)
    fishing_test_round = round(video_count["fliers_action"] * test_ratio)

    tent_setup_train_round = round(video_count["tent_setup"] * train_ratio)
    tent_setup_val_round = round(video_count["tent_setup"] * val_ratio)
    fishing_test_round = round(video_count["tent_setup"] * test_ratio)

    sit_down_bench_train_round = round(video_count["sit_down_bench"] * train_ratio)
    sit_down_bench_val_round = round(video_count["sit_down_bench"] * val_ratio)
    sit_down_bench_test_round = round(video_count["sit_down_bench"] * test_ratio)

    sit_down_floor_train_round = round(video_count["sit_down_floor"] * train_ratio)
    sit_down_floor_val_round = round(video_count["sit_down_floor"] * val_ratio)
    sit_down_floor_test_round = round(video_count["sit_down_floor"] * test_ratio)

    moving_train_round = round(video_count["moving"] * train_ratio)
    moving_val_round = round(video_count["moving"] * val_ratio)
    moving_test_round = round(video_count["moving"] * test_ratio)

    stand_train_round = round(video_count["stand"] * train_ratio)
    stand_val_round = round(video_count["stand"] * val_ratio)
    stand_test_round = round(video_count["stand"] * test_ratio)

    smoking_idx = 0
    fishing_idx = 0
    trash_dump_idx = 0
    wall_over_idx = 0
    damage_to_facilities_idx = 0
    banner_action_idx = 0
    fliers_action_idx = 0
    tent_setup_idx = 0
    sit_down_bench_idx = 0
    sit_down_floor_idx = 0
    moving_idx = 0
    stand_idx = 0


    video_id = 0
    for root, dir, files in os.walk(data_path):

        for filename in files:
            filename_, ext = os.path.splitext(filename)

            if ext == ".mp4":
                split_list = filename_.split("_")
                if split_list[1] == "1":
                    smoking_idx += 1
                    # print(smoking_idx)
                    if smoking_idx <= smoking_train_round:
                        dataset_divide_wr.writerow([filename, "train", video_id])
                    elif smoking_idx > smoking_train_round:
                        if smoking_idx <= smoking_train_round + smoking_val_round:
                            # print("val: ", smoking_idx, smoking_train_round + smoking_val_round)
                            dataset_divide_wr.writerow([filename, "val", video_id])
                        elif smoking_idx > smoking_train_round + smoking_val_round:
                            # print("test: ",smoking_idx, smoking_train_round + smoking_val_round + smoking_test_round)
                            dataset_divide_wr.writerow([filename, "test", video_id])
                elif split_list[1] == "2":
                    fishing_idx += 1
                    if fishing_idx <= fishing_train_round:
                        dataset_divide_wr.writerow([filename, "train", video_id])
                    elif fishing_idx > fishing_train_round:
                        if fishing_idx <= fishing_train_round + fishing_val_round:
                            # print("val: ", smoking_idx, smoking_train_round + smoking_val_round)
                            dataset_divide_wr.writerow([filename, "val", video_id])
                        elif fishing_idx > fishing_train_round + fishing_val_round:
                            # print("test: ",smoking_idx, smoking_train_round + smoking_val_round + smoking_test_round)
                            dataset_divide_wr.writerow([filename, "test", video_id])
                elif split_list[1] == "3":
                    trash_dump_idx += 1
                    if trash_dump_idx <= trash_dump_train_round:
                        dataset_divide_wr.writerow([filename, "train", video_id])
                    elif trash_dump_idx > trash_dump_train_round:
                        if trash_dump_idx <= trash_dump_train_round + trash_dump_val_round:
                            # print("val: ", smoking_idx, smoking_train_round + smoking_val_round)
                            dataset_divide_wr.writerow([filename, "val", video_id])
                        elif trash_dump_idx > trash_dump_train_round + trash_dump_val_round:
                            # print("test: ",smoking_idx, smoking_train_round + smoking_val_round + smoking_test_round)
                            dataset_divide_wr.writerow([filename, "test", video_id])
                elif split_list[1] == "4":
                    wall_over_idx += 1
                    if wall_over_idx <= wall_over_train_round:
                        dataset_divide_wr.writerow([filename, "train", video_id])
                    elif wall_over_idx > wall_over_train_round:
                        if wall_over_idx <= wall_over_train_round + wall_over_val_round:
                            # print("val: ", smoking_idx, smoking_train_round + smoking_val_round)
                            dataset_divide_wr.writerow([filename, "val", video_id])
                        elif wall_over_idx > wall_over_train_round + wall_over_val_round:
                            # print("test: ",smoking_idx, smoking_train_round + smoking_val_round + smoking_test_round)
                            dataset_divide_wr.writerow([filename, "test", video_id])
                elif split_list[1] == "5":
                    damage_to_facilities_idx += 1
                    if damage_to_facilities_idx <= damage_to_facilities_train_round:
                        dataset_divide_wr.writerow([filename, "train", video_id])
                    elif damage_to_facilities_idx > damage_to_facilities_train_round:
                        if damage_to_facilities_idx <= damage_to_facilities_train_round + damage_to_facilities_val_round:
                            # print("val: ", smoking_idx, smoking_train_round + smoking_val_round)
                            dataset_divide_wr.writerow([filename, "val", video_id])
                        elif damage_to_facilities_idx > damage_to_facilities_train_round + damage_to_facilities_val_round:
                            # print("test: ",smoking_idx, smoking_train_round + smoking_val_round + smoking_test_round)
                            dataset_divide_wr.writerow([filename, "test", video_id])
                elif split_list[1] == "6":
                    banner_action_idx += 1
                    if banner_action_idx <= banner_action_train_round:
                        dataset_divide_wr.writerow([filename, "train", video_id])
                    elif banner_action_idx > banner_action_train_round:
                        if banner_action_idx <= banner_action_train_round + banner_action_val_round:
                            # print("val: ", smoking_idx, smoking_train_round + smoking_val_round)
                            dataset_divide_wr.writerow([filename, "val", video_id])
                        elif banner_action_idx > banner_action_train_round + banner_action_val_round:
                            # print("test: ",smoking_idx, smoking_train_round + smoking_val_round + smoking_test_round)
                            dataset_divide_wr.writerow([filename, "test", video_id])
                elif split_list[1] == "7":
                    fliers_action_idx += 1
                    if fliers_action_idx <= fliers_action_train_round:
                        dataset_divide_wr.writerow([filename, "train", video_id])
                    elif fliers_action_idx > fliers_action_train_round:
                        if fliers_action_idx <= fliers_action_train_round + fliers_action_val_round:
                            # print("val: ", smoking_idx, smoking_train_round + smoking_val_round)
                            dataset_divide_wr.writerow([filename, "val", video_id])
                        elif fliers_action_idx > fliers_action_train_round + fliers_action_val_round:
                            # print("test: ",smoking_idx, smoking_train_round + smoking_val_round + smoking_test_round)
                            dataset_divide_wr.writerow([filename, "test", video_id])
                elif split_list[1] == "8":
                    tent_setup_idx += 1
                    if tent_setup_idx <= tent_setup_train_round:
                        dataset_divide_wr.writerow([filename, "train", video_id])
                    elif tent_setup_idx > tent_setup_train_round:
                        if tent_setup_idx <= tent_setup_train_round + tent_setup_val_round:
                            # print("val: ", smoking_idx, smoking_train_round + smoking_val_round)
                            dataset_divide_wr.writerow([filename, "val", video_id])
                        elif tent_setup_idx > tent_setup_train_round + tent_setup_val_round:
                            # print("test: ",smoking_idx, smoking_train_round + smoking_val_round + smoking_test_round)
                            dataset_divide_wr.writerow([filename, "test", video_id])
                elif split_list[1] == "30":
                    sit_down_bench_idx += 1
                    if sit_down_bench_idx <= sit_down_bench_train_round:
                        dataset_divide_wr.writerow([filename, "train", video_id])
                    elif sit_down_bench_idx > sit_down_bench_train_round:
                        if sit_down_bench_idx <= sit_down_bench_train_round + sit_down_bench_val_round:
                            # print("val: ", smoking_idx, smoking_train_round + smoking_val_round)
                            dataset_divide_wr.writerow([filename, "val", video_id])
                        elif sit_down_bench_idx > sit_down_bench_train_round + sit_down_bench_val_round:
                            # print("test: ",smoking_idx, smoking_train_round + smoking_val_round + smoking_test_round)
                            dataset_divide_wr.writerow([filename, "test", video_id])
                elif split_list[1] == "31":
                    sit_down_floor_idx += 1
                    if sit_down_floor_idx <= sit_down_floor_train_round:
                        dataset_divide_wr.writerow([filename, "train", video_id])
                    elif sit_down_floor_idx > sit_down_floor_train_round:
                        if sit_down_floor_idx <= sit_down_floor_train_round + sit_down_floor_val_round:
                            # print("val: ", smoking_idx, smoking_train_round + smoking_val_round)
                            dataset_divide_wr.writerow([filename, "val", video_id])
                        elif sit_down_floor_idx > sit_down_floor_train_round + sit_down_floor_val_round:
                            # print("test: ",smoking_idx, smoking_train_round + smoking_val_round + smoking_test_round)
                            dataset_divide_wr.writerow([filename, "test", video_id])
                elif split_list[1] == "32":
                    moving_idx += 1
                    if moving_idx <= moving_train_round:
                        dataset_divide_wr.writerow([filename, "train", video_id])
                    elif moving_idx > moving_train_round:
                        if moving_idx <= moving_train_round + moving_val_round:
                            # print("val: ", smoking_idx, smoking_train_round + smoking_val_round)
                            dataset_divide_wr.writerow([filename, "val", video_id])
                        elif moving_idx > moving_train_round + moving_val_round:
                            # print("test: ",smoking_idx, smoking_train_round + smoking_val_round + smoking_test_round)
                            dataset_divide_wr.writerow([filename, "test", video_id])
                elif split_list[1] == "33":
                    stand_idx += 1
                    if stand_idx <= stand_train_round:
                        dataset_divide_wr.writerow([filename, "train", video_id])
                    elif stand_idx > stand_train_round:
                        if stand_idx <= stand_train_round + stand_val_round:
                            # print("val: ", smoking_idx, smoking_train_round + smoking_val_round)
                            dataset_divide_wr.writerow([filename, "val", video_id])
                        elif stand_idx > stand_train_round + stand_val_round:
                            # print("test: ",smoking_idx, smoking_train_round + smoking_val_round + smoking_test_round)
                            dataset_divide_wr.writerow([filename, "test", video_id])
                video_id += 1


def used_ffmpeg_video_to_images(data_path, to_data_path):
    for root, dir, files in os.walk(data_path):
        for filename in files:
            filename_, ext = os.path.splitext(filename)
            if ext == ".mp4":
                print("ffmpeg used : " + root + "/" + filename)
                os.makedirs(to_data_path + "/frames/" + filename_, exist_ok=True)
                # command = "ffmpeg -i " + root + "/" + filename + " -f image2 " + to_data_path + "/frames/" + \
                #           filename_ + "/" + filename_ + "_%06d.jpg"

                command = "ffmpeg -i " + root + "/" + filename + " -start_number 1 -threads 4 -b:v 10000k -vsync 0 -an -y -q:v 16 "+ \
                          to_data_path + "/frames/" + filename_ + "/" + filename_ + "_%06d.jpg"

                os.system(command)


def read_frames(to_data_path):
    to_data_path = "/home/di-05/Downloads/hsy/SlowFast/preprocessing"
    os.makedirs(to_data_path + "/frames_list/", exist_ok=True)
    train_csv = open(to_data_path + "/frames_list/train_frames.csv", 'w', newline='')
    train_wr = csv.writer(train_csv)
    train_wr.writerow(["original_video_id video_id frame_id path labels"])

    test_csv = open(to_data_path + "/frames_list/test_frames.csv", 'w', newline='')
    test_wr = csv.writer(test_csv)
    test_wr.writerow(["original_video_id video_id frame_id path labels"])

    val_csv = open(to_data_path + "/frames_list/val_frames.csv", 'w', newline='')
    val_wr = csv.writer(val_csv)
    val_wr.writerow(["original_video_id video_id frame_id path labels"])

    dataset_divide_csv = open(to_data_path + "/dataset_divide.csv", 'r')
    dataset_divide_rd = csv.reader(dataset_divide_csv)
    dataset_list = []
    for line in dataset_divide_rd:
        # if line[0].split("_")[1] == "3" or line[0].split("_")[1] == "7":
        #     print(line)
        #     dataset_list.append(line)
        dataset_list.append(line)

    video_id = 0
    video_list = []
    frame_number = 0
    check_video_id = False
    file_list = []
    for root, dir, files in os.walk(to_data_path + "/frames"):
        for filename in files:
            file_list.append(root + "/" + filename)

        file_list.sort()

    for file_name in file_list:
        print("read_frames : ", file_name)

        if file_name.split("/")[-2] not in video_list:
            video_list.append(file_name.split("/")[-2])
            # video_id += 1
            check_video_id = True

        for i in range(len(dataset_list)):
            if file_name.split("/")[-2] == dataset_list[i][0].split(".")[0]:
                if dataset_list[i][1] == "train":
                    if check_video_id == True:
                        frame_number = 0
                    train_wr.writerow([str(dataset_list[i][0].split(".")[0]) + " " + str(dataset_list[i][2]) + " " + \
                                       str(frame_number) + " " + str(file_name) + " " + "''"])
                    frame_number += 1
                    check_video_id = False

                elif dataset_list[i][1] == "val":
                    if check_video_id == True:
                        frame_number = 0
                    val_wr.writerow([str(dataset_list[i][0].split(".")[0]) + " " + str(dataset_list[i][2]) + " " + \
                                     str(frame_number) + " " + str(file_name) + " " + "''"])
                    frame_number += 1
                    check_video_id = False

                elif dataset_list[i][1] == "test":
                    if check_video_id == True:
                        frame_number = 0
                    test_wr.writerow([str(dataset_list[i][0].split(".")[0]) + " " + str(dataset_list[i][2]) + " " + \
                                      str(frame_number) + " " + str(file_name) + " " + "''"])
                    frame_number += 1
                    check_video_id = False


def json_parsing(root, filename, writer, predict_writer, check_flag):
    filename_, ext = os.path.splitext(filename)

    with open(root + "/" + filename, 'r', encoding='UTF-8') as jsonfile:
        json_data = json.load(jsonfile)

    annotations = json_data["annotations"]
    info = json_data["info"]
    image_width = info["width"]
    image_height = info["height"]

    events = json_data["events"]

    events_list = []

    for event in events:
        ev_object_id = event["object_id"]
        ev_actor_id = event["actor_id"]
        ev_start_frame = event["ev_start_frame"]
        ev_end_frame = event["ev_end_frame"]
        events_list.append([ev_object_id, ev_actor_id, ev_start_frame, ev_end_frame])

    actor_id = 0

    for i in range(len(events_list)):
        start_frame = events_list[i][2]
        end_frame = events_list[i][3]
        actor_id += 1

        sec = 0
        for annotation in annotations:
            class_id = annotation["object_id"]
            # if class_id == 3 or class_id == 7:
            cur_frame = annotation["cur_frame"]

            frame_to_sec = math.floor(cur_frame / 3)
            if sec != frame_to_sec:
                sec = frame_to_sec
                if class_id == events_list[i][0]:
                    if annotation["actor_id"] == events_list[i][1]:
                        if cur_frame >= start_frame and cur_frame <= end_frame:
                            bbox = annotation["bbox"]
                            xtl = bbox[0][0]
                            ytl = bbox[0][1]
                            xbr = bbox[1][0]
                            ybr = bbox[1][1]
                            x1 = round(xtl / image_width, 4)
                            y1 = round(ytl / image_height, 4)
                            x2 = round(xbr / image_width, 4)
                            y2 = round(ybr / image_height, 4)

                            # AVA 데이터 셋에 맞도록 넘버링: 3개의 class 에 대해 1 ~ 3
                            if class_id == 3:
                                class_id = 1
                            elif class_id == 7:
                                class_id = 2
                            elif class_id == 4:
                                class_id = 3

                            writer.writerow([filename_, frame_to_sec, x1, y1, x2, y2, class_id, actor_id])
                            if check_flag == "val":
                                predict_writer.writerow([filename_, frame_to_sec, x1, y1, x2, y2, '', 0.9])

    # Smoking info
    # with open(root + "/" + filename, 'r', encoding='UTF-8') as jsonfile:
    #     json_data = json.load(jsonfile)
    #
    # annotations = json_data["annotations"]
    # info = json_data["info"]
    # image_width = info["width"]
    # image_height = info["height"]
    #
    # events = json_data["events"]
    #
    # events_list = []
    #
    # for event in events:
    #     ev_object_id = event["object_id"]
    #     ev_actor_id = event["actor_id"]
    #     ev_start_frame = event["ev_start_frame"]
    #     ev_end_frame = event["ev_end_frame"]
    #     events_list.append([ev_object_id, ev_actor_id, ev_start_frame, ev_end_frame])

    # for annotation in annotations:
    #     class_id = annotation["object_id"]
    #
    #     if class_id == 30:
    #         class_id = 9
    #     elif class_id == 31:
    #         class_id = 10
    #     elif class_id == 32:
    #         class_id = 11
    #     elif class_id == 33:
    #         class_id = 12
    #
    #     if class_id == 3 or class_id == 7:
    #         bbox = annotation["bbox"]
    #         actor_id = annotation["actor_id"]
    #
    #     bbox = annotation["bbox"]
    #     actor_id = annotation["actor_id"]
    #     cur_frame = annotation["cur_frame"]
    #     # print(class_id, bbox)
    #     xtl = bbox[0][0]
    #     ytl = bbox[0][1]
    #     xbr = bbox[1][0]
    #     ybr = bbox[1][1]
    #     x1 = round(xtl / image_width, 4)
    #     y1 = round(ytl / image_height, 4)
    #     x2 = round(xbr / image_width, 4)
    #     y2 = round(ybr / image_height, 4)
    #     # writer.writerow([filename_, cur_frame, x1, y1, x2, y2, class_id, actor_id])
    #     # if check_flag == "val":
    #     #     predict_writer.writerow([filename_, cur_frame, x1, y1, x2, y2, '', 0.9])
    #     frame_to_sec = math.floor(cur_frame / 3)
    #     writer.writerow([filename_, frame_to_sec, x1, y1, x2, y2, class_id, actor_id])
    #     if check_flag == "val":
    #         predict_writer.writerow([filename_, frame_to_sec, x1, y1, x2, y2, '', 0.9])


def read_json(data_path, to_data_path):
    os.makedirs(to_data_path + "/annotations/", exist_ok=True)
    train_csv = open(to_data_path + "/annotations/train.csv", 'w', newline='')
    train_wr = csv.writer(train_csv)

    test_csv = open(to_data_path + "/annotations/test.csv", 'w', newline='')
    test_wr = csv.writer(test_csv)

    val_csv = open(to_data_path + "/annotations/val.csv", 'w', newline='')
    val_wr = csv.writer(val_csv)

    val_predict_csv = open(to_data_path + "/annotations/val_predict.csv", 'w', newline='')
    val_predict_wr = csv.writer(val_predict_csv)

    dataset_read_csv = open(to_data_path + "/dataset_divide.csv", 'r')
    dataset_file = csv.reader(dataset_read_csv)
    dataset_list = []
    writer = ""
    predict_writer = ""
    check_flag = ""

    for line in dataset_file:
        # if line[0].split("_")[1] == "3" or line[0].split("_")[1] == "7" or line[0].split("_")[1] == "4":
        #     dataset_list.append(line)
        dataset_list.append(line)

    for root, dir, files in os.walk(data_path):
        for filename in files:
            filename_, ext = os.path.splitext(filename)
            if ext == ".json":
                print("read_json : ", filename)
                for i in range(len(dataset_list)):
                    if filename_ == dataset_list[i][0].split(".")[0]:
                        if dataset_list[i][1] == "train":
                            writer = train_wr

                        elif dataset_list[i][1] == "val":
                            check_flag = "val"
                            writer = val_wr
                            predict_writer = val_predict_wr

                        elif dataset_list[i][1] == "test":
                            writer = test_wr

                        json_parsing(root, filename, writer, predict_writer, check_flag)
                check_flag = ""

def rm_jpg(to_data_path):
    for root, dir, files in os.walk(to_data_path + "/frames"):
        for filename in files:
            filename_, ext = os.path.splitext(filename)

            if ext == ".jpg":
                if filename_.split("_")[-1] == "000000":
                    print(filename_)
                    os.remove(root + "/" + filename)

def copy_completed_mp4(mv_data_path):
    filtering_folder = ["1단계", "2단계", "초기데이터"]
    completed_json_path = "Z:/slowfast_train/completed_json"
    video_path = "Z:/1.Data/1.불법행위"
    json_file_txt = open(completed_json_path + "/json_list.txt", 'w')

    json_list = []
    json_root_list = []

    for root, dirs, files in os.walk(completed_json_path):
        for file in files:
            filename, ext = os.path.splitext(file)
            if ext == ".json":
                print("completed_json : ", file)
                json_list.append(file.split(".")[0])
                # json_file_txt.write(root + "/" + file + "\n")

    for root, dirs, files in os.walk(video_path):
        dirs[:] = [dir for dir in dirs if dir.lower() not in filtering_folder]

        for file in files:
            filename, ext = os.path.splitext(file)

            if ext == ".mp4":
                if filename in json_list:
                    print("copy_file : ", file)
                    if filename.split("_")[1] == "3":
                        os.makedirs(mv_data_path + "/C_3_trash_dump", exist_ok=True)
                        shutil.copy(root + "/" + file, mv_data_path + "/C_3_trash_dump")
                    elif filename.split("_")[1] == "7":
                        os.makedirs(mv_data_path + "/C_7_fliers_action", exist_ok=True)
                        shutil.copy(root + "/" + file, mv_data_path + "/C_7_fliers_action")
                    elif filename.split("_")[1] == "4":
                        os.makedirs(mv_data_path + "/C_4_wall_over", exist_ok=True)
                        shutil.copy(root + "/" + file, mv_data_path + "/C_4_wall_over")
                    elif filename.split("_")[1] == "2":
                        os.makedirs(mv_data_path + "/C_2_fishing", exist_ok=True)
                        shutil.copy(root + "/" + file, mv_data_path + "/C_2_fishing")
                    elif filename.split("_")[1] == "1":
                        os.makedirs(mv_data_path + "/C_1_smoking", exist_ok=True)
                        shutil.copy(root + "/" + file, mv_data_path + "/C_1_smoking")


def main():
    data_path, to_data_path = parser_init()
    # dataset_divide(data_path, to_data_path)
    # used_ffmpeg_video_to_images(data_path, to_data_path)

    read_frames(to_data_path)
    read_json(data_path, to_data_path)

    # Move files
    # copy_completed_mp4(mv_data_path="Z:/slowfast_train/completed_video")

    # rm_jpg(to_data_path)


if __name__ == '__main__':
    main()