import os
import json
import jsonschema
from jsonschema import validate

folder_path = r"C:\Users\Administrator\Desktop\label\label_test"

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

def json_validator(data, schema):
    
    try:
        validate(data, schema)
    except jsonschema.ValidationError as ve :
        print(ve.message)
        return False

with open("./schema.txt", 'w', encoding='utf8') as error_f:
    for (root, dirs, files) in os.walk(folder_path):
        for file in files:
            filename , ext = os.path.splitext(file)
            if ext == ".json":
                with open(root + "/" + file, 'r', encoding='utf8') as json_f:

                        json_data = json.load(json_f)
                        # print(json_validator(json_data, json_schema))
                        result = json_validator(json_data, json_schema)

                        if result == False:
                            error_f.write(filename +'\n')