import os

def ffmpeg_process(video_path, output_path):

    arr = os.listdir(video_path)
    empty = []
    file_name = None

    for i in range(len(arr)):
        empty.append(arr[i].split('.'))

    for i in range(len(arr)):
        if len(empty[i]) == 2:
            if empty[i][1] == 'mp4' or empty[i][1] == 'avi':
                print(empty[i])
                file_name = empty[i][0]+'.'+empty[i][1]
                print(file_name)

    cmd = f'ffmpeg -ss 00:00:0 -i {video_path}/{file_name} -r 0.05 {output_path}/%5d.jpg'
    print(f'cmd:{cmd}')
    os.system(cmd)
