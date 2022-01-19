import os
import inspect

def yolo(original_files, prediction_files='/inference/output'):
    print('yolo.py/ getcwd >>> ' + os.getcwd())
    print(f'inspect.getfile(yolo):{inspect.getfile(yolo)}')
    path = os.path.dirname(inspect.getfile(yolo))  #PyTorch_YOLOv4 절대경로 나옴
    
    #detect.py 실행코드
    cmd = 'python3 '+ path +'/detect.py'
    
    # + args
    cmd = cmd + ' --weights '+ path +'/weights/yolov4-csp-x-leaky.weights ' + \
        ' --source ' + original_files + '/input_images' \
        ' --output ' + prediction_files + \
        ' --cfg '+ path +'/models/yolov4-csp-x-leaky.cfg ' + \
        ' --device cpu' + \
        ' --classes ' + '0 2 3 5 7' + \
        ' --names ' + path + '/data/coco.names'
    
    print("yolo() cmd >>> " , cmd)
    os.system(cmd)