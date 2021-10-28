import os
import subprocess
import pandas as pd
import shutil

folder_path = "C:\\Users/user/Desktop/영상/raw_video"
save_path = "C:\\Users/user/Desktop/영상/frame/"

for root, dirs, files in os.walk(folder_path):
    for file in files:
        file_name, extension = os.path.splitext(file)
        subprocess.run("ffmpeg -i " + root + "/" + file + " -r 3 " + save_path + file_name + "-r3.mp4")

path = r"C:\Users\user\Desktop\영상\raw_video"
shutil.rmtree(path)

frame_folder = "C:\\Users/user/Desktop/영상/frame/"
save_folder = "C:\\Users/user/Desktop/영상/split/"
day_dict = {0:"mon",1:"tue",2:"wed",3:"thu",4:"fri",5:"sat",6:"sun"}
# ffmpeg -ss 00:00 -i 2021-08-02_06-00-00_mon_sunny_out_ja-ma_C0064-r3.mp4 -to 03:00 2021-08-02_06-00-00_mon_sunny_out_ja-ma_C0041.mp4

for root, dirs, files in os.walk(frame_folder):
    for file in files:
        temp = pd.Timestamp(file[13:17] + "-" + file[17:19] + "-" + file[19:21])
        for i in range(0, 20):
            start_time = '%02d' % (i * 3)
            # end_time = '%02d' % ((i + 1) * 3)
            subprocess.run('ffmpeg -ss ' + start_time + ':00 -i ' + root + "/" + file + ' -to 03:00 '
                           + save_folder +
                           file[13:17] + "-" + file[17:19] + "-" + file[19:21] + "_" + file[21:23] + "-"
                           + start_time + '-00_' + day_dict[temp.dayofweek] + '_sunny_out_ja-ma_C0041.mp4')