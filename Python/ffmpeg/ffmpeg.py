import os
import subprocess
import pandas as pd

dir_path = r"C:\Users\Administrator\Desktop\python\low_video"
workdir = os.path.dirname(os.path.realpath(__file__))

pass_list = ['./frame','./split']
for path in pass_list:
    os.mkdir(path)

num_to_day = {0 : 'mon', 1 : 'tue', 2 : 'wed', 3 : 'thu', 4 : 'fri', 5 : 'sat', 6 : 'sun'}

for(root, dirs, files) in os.walk(dir_path):
    for file in files:
        if file.split(".")[-1].lower() == "mp4":
            year = file[13:17]
            month = file[17:19]
            day = file[19:21]
            time = file[21:23]
            gong = file[39:41]
            arr = "mon_sunny_out_ja-ma_C0041"
            s= pd.Timestamp(int(year), int(month), int(day))
            yoil = s.dayofweek
            yoil_1 = num_to_day[yoil]
            result = subprocess.Popen(['ffmpeg','-y','-i',workdir + '\\low_video\\'+ file, '-r', '3',workdir +'./frame'+ '/test_frame' +'.mp4'],stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            out, err = result.communicate()
            exitcode = result.returncode
            print('frame Completed')               
    my_time = 0
    for file in files:
        if file.split(".")[-1].lower() == "mp4":
            while True:
                result_split = subprocess.Popen(['ffmpeg','-y','-i',workdir + '\\frame\\test_frame.mp4', '-ss', '%02d' %(my_time)+':00', '-t','03:00' ,workdir + '\\split\\'+ year+'-'+month+'-'+day +'_'+ time + '-'+'%02d' %(my_time)+'-'+gong+'_'+yoil_1+'_'+arr+'.mp4'],stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                out, err = result_split.communicate()
                exitcode_split = result_split.returncode
                my_time = my_time + 3
                if my_time == 60: break
                print('split Completed :',my_time)