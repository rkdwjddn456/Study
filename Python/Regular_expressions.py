import re
import os
import json

folder_path = r"C:\Users\Administrator\Desktop\label\label_test"

weather = ("snowy", "rainy", "cloudy")
day = ["mon", "tue", "wed", "thu", "fri", "sat", "sun"]
in_out = ["in", "out"]
extension = ".mp4"

with open("./filename_error.txt", 'w', encoding='utf8') as error_f:
    for (root, dirs, files) in os.walk(folder_path):
        for file in files:
            filename, ext = os.path.splitext(file)
            if ext == ".json":
                with open(root + "/" + file, 'r', encoding='utf8') as json_f:
                            json_data = json.load(json_f)
                            name = json_data["video"]["file_name"]

                            year = re.compile("\d{4}-\d{2}-\d{2}_\d{2}-\d{2}-\d{2}")
                            year_input = [name[0:4] + '-'+ name[5:7] + '-' + name[8:10] + '_' + name[11:13] + '-' + name[14:16] + '-' + name[17:19]]
                            year_validation = year.search(str(year_input).replace(" ",""))
                            day_validation = re.search(name[20:23], str(day))
                            weather_validation = re.search(name[24:27], str(weather))
                            in_out_validation = re.search(name[30:33], str(in_out))
                            ext_validation = re.search(name[45:], str(extension))

                            if year_validation:
                                print("year and month are good")
                            else:
                                error_f.write("year and month are bad => " + filename +'\n')

                            if day_validation:
                                print("day is good")
                            else:
                                error_f.write("day are bad =>" + filename +'\n')                                
                            
                            if weather_validation:
                                print("weather is good")
                            else:
                                error_f.write("weather are bad => " + filename +'\n')

                            if in_out_validation:
                                print("in_out is good")
                            else:
                                error_f.write("in_out is bad => " + filename +'\n')

                            if ext_validation:
                                print("ext is good")
                            else:
                                error_f.write("ext is bad =>" + filename +'\n')                         