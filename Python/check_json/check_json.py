import os

# zip파일 지우기

zip_path = r"C:\Users\Administrator\Desktop\label\label_test"

for (root, dirs, files) in os.walk(zip_path):
    for file in files:
        ext = os.path.splitext(file)[-1]
        if ext.lower() =='.zip':
            os.remove("%s%s"%(root +'\\',file))

# mp4파일과 json파일이 같이 존재하는지 찾기

file_path = r"C:\Users\Administrator\Desktop\label\label_test\2021-09-06\team6"

for(root, dirs, files) in os.walk(file_path):
    for dir_name in dirs:
        same_path = os.listdir(file_path + '\\' + dir_name)
        if len(same_path) % 2 != 0:
            print('mp4와 json파일이 같이 존재 하지 않는 path :',file_path + '\\' + dir_name)
            
# 중복 파일 찾기

folder_path = r"C:\Users\Administrator\Desktop\label\label_test"

file_list = []

for (root, dirs, files) in os.walk(folder_path):
    for file in files:
        file_name, extension = os.path.splitext(file)
        if extension == ".json" or extension == ".mp4":
            if file in file_list:
                print('중복 파일이 존재하는 path :',file)
            else:
                file_list.append(file)

# 파일명 규칙 위반

day_list = ['mon', 'tue', 'wed', 'thu', 'fri', 'sat' , 'sun']

for(root, dirs, files) in os.walk(folder_path):
    for file in files:
        file_name = os.path.splitext(file)
        name = file_name[0]
        
        if len(name) != 45:
            print("규칙명 위반한 Path :",root)
            print("규칙명 위반한 파일 :",file)
        elif name[24:45] != 'sunny_out_ja-ma_C0041':
            print("규칙명 위반한 Path :",root)
            print("규칙명 위반한 파일 :",file)
        elif name[20:23] not in day_list:
            print("규칙명 위반한 Path :",root)
            print("규칙명 위반한 파일 :",file)