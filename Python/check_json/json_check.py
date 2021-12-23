import os

file_path = "C:/Users/Administrator/Desktop/python/json_2"
json_path = "C:/Users/Administrator/Desktop/python/json_list.txt"

file_list = []

for root, dirs, files in os.walk(file_path):
    for file in files:
        file_list.append(file.split(".")[0])

with open("./error.txt", 'w', encoding='utf8') as error_f:
    with open(json_path, 'r', encoding='utf8') as json_list:
        line = None
        while line != '':
            line = json_list.readline().replace('\n','')
            if line not in file_list:
                error_f.write(line+'\n')