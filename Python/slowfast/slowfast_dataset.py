import os
import subprocess
import json


def createFolder(directory):
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
    except OSError:
        print('Error: Creating directory. ' + directory)


def load_json_event(json_path):
    events = []
    if os.path.exists(json_path):
        with open(json_path, 'r', encoding='utf8') as json_f:
            json_data = json.load(json_f)

            events = json_data["events"]
    else:
        with open("./error.txt", 'w', encoding='utf8') as error_f:
            error_f.write(json_path + "\n")
        print("Error : not matched " + json_path)

    return events


def write_csv(output_dir, class_no, output_mp4):
    global split_dict

    output_mp4 = r"/mnt/learning_mount/slowfast_train/preprocessing_kinetic/data/kinetic_fmt/" + output_mp4

    if int(class_no) >= 30:
        class_no = str(int(class_no) - 22)
    else:
        class_no = str(int(class_no) - 1)

    if split_dict[class_no] % 10 == 0:
        with open(output_dir + "test.csv", "a", encoding='utf8') as test_f:
            test_f.write(output_mp4 + " " + class_no + "\n")
        split_dict[class_no] = 1
    elif split_dict[class_no] % 9 == 0:
        with open(output_dir + "val.csv", "a", encoding='utf8') as val_f:
            val_f.write(output_mp4 + " " + class_no + "\n")
        split_dict[class_no] += 1
    else:
        with open(output_dir + "train.csv", "a", encoding='utf8') as train_f:
            train_f.write(output_mp4 + " " + class_no + "\n")
        split_dict[class_no] += 1


def run_ffmpeg(events, json_path, file_name):
    if len(events) != 0:
        global output_dir
        count = 1
        class_no = file_name.split("_")[1]
        if class_no in class_dict.keys():
            createFolder(output_dir + class_dict[class_no])
        for event in events:
            input_mp4 = json_path.replace("json", "mp4")
            output_mp4 = class_dict[class_no] + "/" + file_name + "_%03d.mp4"% (count)
            count += 1
            cmd = 'ffmpeg -n -i ' + input_mp4 + ' -an -compression_algo raw -r 3 -filter_complex select=between(n\\,' \
                  + str(event["ev_start_frame"]) + '\\,' + str(event["ev_end_frame"]) + '\\),setpts=PTS-STARTPTS ' + output_dir + output_mp4
            print(cmd)
            subprocess.run(cmd)  # 처리는 이미 subprocess 에서 실행이 되고, 쉘에 보이는 결과는 사용할 필요가 없음
            write_csv(output_dir, class_no, output_mp4)


def processing(label_folder):
    for root, dirs, files in os.walk(label_folder):
        for file in files:
            file_name, extension = os.path.splitext(file)
            if extension.lower() == ".json":
                print(file)
                json_path = root + "/" + file
                events = load_json_event(json_path)

                run_ffmpeg(events, json_path, file_name)


if __name__ == "__main__":
    class_dict = {"1": "smoking", "2": "fishing", "3": "trash_dump", "4": "wall_over", "5": "damage_to_facilities", "6": "banner_action",
                  "7": "fliers_action", "8": "tent_setup", "30": "sit_down_bench", "31": "sit_down_floor", "32": "moving", "33": "stand"}
    # "class": 갯수
    split_dict = {"0": 1, "1": 1, "2": 1, "3": 1, "4": 1, "5": 1,
                  "6": 1, "7": 1, "8": 1, "9": 1, "10": 1, "11": 1}

    output_dir = r"Y:/slowfast_train/preprocessing_kinetic/data/kinetic_fmt/"
    label_folder = r"Y:/slowfast_train/completed_video2/"
    createFolder(output_dir)

    processing(label_folder)