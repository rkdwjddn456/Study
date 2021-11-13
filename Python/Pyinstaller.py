from jsonschema import validate
import json
import os
import re
from operator import itemgetter

json_schema = {
  "title": "test",
  "version": 1,
  "type": "object",
  "properties": {
    "info" : {
      "type" : "object",
      "properties" : {
        "year" : {
          "type" : "string", "pattern": "\d{4}"
        },
        "date_created" : {
          "type" : "string", "pattern": "\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}"
        },
        "weather" : {
          "type" : "string", "enum": ["sunny", "snowy", "rainy", "cloudy"]
        },
        "version" : {
          "type" : "string"
        },
        "day" : {
          "type" : "string", "enum": ["mon", "tue", "wed", "thu", "fri", "sat", "sun"]
        },
        "username" : {
          "type" : "string"
        }
      }
    },

    "video" : {
      "type" : "object",
      "properties" : {
        "total_person" : {
          "type" : "number", "minimum": 5
        },
        "in_out" : {
          "type" : "string", "enum": ["in", "out"]
        },
        "file_name" : {
          "type" : "string"
        },
        "fps" : {
          "type" : "number", "minimum": 3
        },
        "location" : {
          "type" : "string", "enum": ["jagalchi-market", "seomyeon-yk-front", "sajik-stadium-commercial-area", "junggu-jungangdong-around",
                                      "dongrae-station-around", "sasang-intercity-bus-terminal","yeonsandong-makgeolli-alley"]
        },
        "resolution" : {
          "type" : "array",
          "items" : {
              "type" : "number"
          }
        },
        "location_type" : {
          "type" : "string", "enum": ["downtown", "station/apartment", "office", "station", "station/downtown", "alley"]
        },
        "total_frame" : {
          "type" : "number", "minimum": 540
        },
        "play_time" : {
          "type" : "string", "pattern": "\d{2}:\d{2}:\d{2}"
        }
      }
    },

    "annotations": {
      "type": "array",
      "items": {
          "type": "object",
          "properties": {
            "id": {
              "type": "string"
            },
            "frame": {
              "type": "number"
            },
            "bbox": {
              "type": "array",
                "items": {
                  "type": "number"
                }
            },
            "direction": {
              "type": "string", "enum": ["N", "NE", "E", "SE", "S", "SW", "W", "NW"]
            },
            "top_type": {
              "type": "string", "enum": ["long_sleeve", "short_sleeve", "sleeveless", "onepice"]
            },
            "top_color": {
              "type": "string",
              "enum": ["red", "orange", "yellow", "green", "blue", "purple", "pink", "brown", "white", "grey", "black"]
            },
            "bottom_type": {
              "type": "string", "enum": ["long_pants", "short_pants", "skirt", "none"]
            },
            "bottom_color": {
              "type": "string",
              "enum": ["red", "orange", "yellow", "green", "blue", "purple", "pink", "brown", "white", "grey", "black","none"]
            },
            "accessories": {
              "type": "string", "enum": ["carrier", "umbrella", "bag", "hat", "glasses", "none"]
            },
            "pet": {
              "type": "integer", "minimum": 0, "maximum": 1
            },
            "state": {
              "type": "string", "enum": ["forward", "backward", "parking"]
            }
          }
      }
    },

    "events" : {
      "type" : "array",
      "items" : {
          "type" : "object",
          "properties" : {
            "action_position" : {
              "type" : "string"
            },
            "end_frame" : {
              "type" : "number"
            },
            "start_frame" : {
              "type" : "number"
            },
            "action" : {
              # "type" : "string", "enum": ["store_in", "store_out", "window_shopping", "buy", "sale", "tasting"]
              "type" : "string", "enum": ["store_in", "store_out"]
            },
            "id" : {
              "type" : "string", "pattern": "person_\d{1,}$"
            }
          }
      }
    },

    "categories" : {
      "type" : "array",
      "items" : {
          "type" : "object",
          "properties" : {
            "supercategory" : {
              "type" : "string", "enum": ["person", "actor"]
            },
            "id" : {
              "type" : "string"
            },
            "gender" : {
              "type" : "string", "enum": ["male", "female"]
            },
            "age": {
              "type": "string", "enum": ["child", "teenager", "adult", "senior"]
            },
            "cam_in" : {
              "type" : "number"
            },
            "cam_in_direction": {
              "type": "string", "enum": ["N", "NE", "E", "SE", "S", "SW", "W", "NW"]
            },
            "cam_out" : {
              "type" : "number"
            },
            "cam_out_direction": {
              "type": "string", "enum": ["N", "NE", "E", "SE", "S", "SW", "W", "NW"]
            }
          }
      }
    },

    "background": {
      "type": "array",
      "items": {
          "type": "object",
          "properties": {
            "parking": {
              "type": "integer", "minimum": 0, "maximum": 1
            },
            "toilet": {
              "type": "integer", "minimum": 0, "maximum": 1
            },
            "elevator": {
              "type": "integer", "minimum": 0, "maximum": 1
            },
            "supercategory": {
              "type": "string","enum": ["store", "car"]
            },
            "segmentation": {
              "type": "array",
              "items": {
                  "type": "array",
                  "items": {
                    "type": "number"
                  }
              }
            },
            "id": {
              "type": "string"
            },
            "category": {
              "type": "string", "enum": ["accommodation", "restaurant", "repair", "service",
                                         "wholesale_retail", "sports", "education", "rental", "realty", "none"]
            },
            "floor": {
              "type": "string"
            },
            "empty": {
              "type": "integer", "minimum": 0, "maximum": 1
            }
          }
      }
    },
  }
}

def check_json_fmt(folder_path):    # 구문 검사
  error_count = 0
  with open("./fmt_error.txt", 'w', encoding='utf8') as error_f:
    for root, dirs, files in os.walk(folder_path):
      for file in files:
        file_name, extension = os.path.splitext(file)
        if extension == ".json":
          with open(root + "/" + file, encoding="utf8") as json_file:
            print(file)
            json_data = json.load(json_file)
            try:
              validate(schema=json_schema, instance=json_data)
            except Exception as e:
              error_count += 1
              error_f.write(root + "/" + file + " : \n")
              error_f.write(str(e) + "\n\n\n")
  print(error_count)

def check_double(folder_path):  # 파일 중복성 검사
  file_list = []
  with open("./double_error.txt", 'w', encoding='utf8') as error_f:
    for root, dirs, files in os.walk(folder_path):
      for file in files:
        file_name, extension = os.path.splitext(file)
        if extension == ".json":
          if file in file_list:
            print(file)
            error_f.write(file + "\n")
          else:
            file_list.append(file)

def check_match(folder_path):   # json & mp4 pair 검사
  with open("./match_error.txt", 'w', encoding='utf8') as error_f:
    for root, dirs, files in os.walk(folder_path):
      for file in files:
        file_name, extension = os.path.splitext(file)
        if extension == ".json":
          if not os.path.exists(root + "/" + file_name + ".mp4"):
            print(file)
            error_f.write(file + "\n")
        else:
          if not os.path.exists(root + "/" + file_name + ".json"):
            print(file)
            error_f.write(file + "\n")

def check_file_name(folder_path):   # 파일명 규칙 검사
  pattern = "2021-[0-1]\d-[0-3]\d_[0-2]\d-[0-6]\d-00_(mon|tue|wed|thu|fri|sat|sun)_(sunny|snowy|rainy|cloudy)_out_(ja-ma|se-yk|sa-st|ju-ja|do-sa|sa-bt|ye-ma)_"
  with open("./name_error.txt", 'w', encoding='utf8') as error_f:
    for root, dirs, files in os.walk(folder_path):
      for file in files:
        file_name, extension = os.path.splitext(file)
        if extension == ".json":
          result = re.match(pattern, file_name)
          if result == None:
            print(file)
            error_f.write(file+"\n")

def remove_zip_file(folder_path):
  for root, dirs, files in os.walk(folder_path):
    for file in files:
      file_name, extension = os.path.splitext(file)
      if extension.lower() == ".zip":
        os.remove(root + "/" + file)

def statistics(floder_path):
    person_count = {
      'male': 0,
      'female': 0,
      'child': 0,
      'teenager': 0,
      'adult': 0,
      'senior': 0,
      'long_sleeve': 0,
      'short_sleeve': 0,
      'sleeveless': 0,
      'onepice': 0,
      'top_red': 0,
      'top_orange': 0,
      'top_yellow': 0,
      'top_green': 0,
      'top_blue': 0,
      'top_purple': 0,
      'top_pink': 0,
      'top_brown': 0,
      'top_white': 0,
      'top_grey': 0,
      'top_black': 0,
      'long_pants': 0,
      'short_pants': 0,
      'skirt': 0,
      'bottom_type_none': 0,
      'bottom_red': 0,
      'bottom_orange': 0,
      'bottom_yellow': 0,
      'bottom_green': 0,
      'bottom_blue': 0,
      'bottom_purple': 0,
      'bottom_pink': 0,
      'bottom_brown': 0,
      'bottom_white': 0,
      'bottom_grey': 0,
      'bottom_black': 0,
      'bottom_color_none': 0,
      'carrier': 0,
      'umbrella': 0,
      'bag': 0,
      'hat': 0,
      'glasses': 0,
      'acc_none': 0,
      'pet': 0
    }

    filtering_folder = []

    for root, dirs, files in os.walk(floder_path):
      dirs[:] = [dir for dir in dirs if dir.lower() not in filtering_folder]
      for file in files:
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
                annotation["gender"] = \
                  [category["gender"] for category in categories if category["id"] == annotation["id"]][0]
                annotation["age"] = \
                  [category["age"] for category in categories if category["id"] == annotation["id"]][0]
                process_annotations.append(annotation)

          for process_annotation in process_annotations:
            person_count[process_annotation["gender"]] += 1
            person_count[process_annotation["age"]] += 1
            person_count[process_annotation["top_type"]] += 1
            person_count["top_" + process_annotation["top_color"]] += 1

            bottom_type = process_annotation["bottom_type"]
            if bottom_type == "none":
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

if __name__ == "__main__":
    folder_path = input("탐색할 폴더 지정 : ")
    mode = int(input('1 : Json 구문 정확성 검사\n2 : 파일 중복성 검사\n3 : mp4, Json 매칭 검사'
                 '\n4 : 파일명 규칙 검사\n5 : 통계\n: '))

    print("folder_path : " + folder_path)
    print("mode : " + mode)

    # folder_path = "\\\\192.168.101.201\\0.공유폴더\\json데이터"
    # mode = 4

    if mode == 1:
      check_json_fmt(folder_path)
    elif mode == 2:
      check_double(folder_path)
    elif mode == 3:
      check_match(folder_path)
    elif mode == 4:
      check_file_name(folder_path)
    elif mode == 5:
      try:
        statistics(folder_path)
      except Exception as e:
        print(e)

    print("Done")

    while True:
      continue