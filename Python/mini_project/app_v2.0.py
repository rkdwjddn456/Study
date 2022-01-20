#  -*- coding: utf-8 -*-
import os
from werkzeug.utils import redirect
from flask import Flask, request
from PyTorch_YOLOv4.yolo import yolo
from FFmpeg.ffmpeg_ import ffmpeg_process

app = Flask(__name__)

@app.route('/fileupload_QT/<now>', methods=['post'])
def file_upload_qt(now):
    files = request.files.getlist("file")
    print(f'file uploaded!!!!{files}')
    os.makedirs(f'static/qt/{now}/input_images', exist_ok=True)
    os.makedirs(f'static/qt/{now}/output_images', exist_ok=True)

    for file in files:
        file.save(os.path.join(f'/test_final/static/qt/{now}' , file.filename))
    
    ffmpeg_process(f'/test_final/static/qt/{now}', f'static/qt/{now}/input_images')
    yolo(f'/test_final/static/qt/{now}/', f'static/qt/{now}/output_images')

    return redirect(f'https://www.naver.com') # 의미없음

if __name__ == "__main__":
     app.run(host='0.0.0.0', port='5000', debug=True)