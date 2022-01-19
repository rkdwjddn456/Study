import sys
import requests
import os
import cv2
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import QImage, QPixmap

class Thread1(QThread):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
    
    def run(self):
        files = open(fname[0], 'rb')
        upload = {'file': files}
        # res = requests.post('http://192.168.0.103:5000/file_upload', files= upload)
        res = requests.post('http://192.168.25.44:5000/fileupload_QT', files= upload)

class Thread2(QThread):
    changePixmap = pyqtSignal(QImage)
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
    
    def run(self):
        global running, count, start_frame_number
        cap = cv2.VideoCapture(fname[0])
        fps = cap.get(cv2.CAP_PROP_FPS)
        frame_count = cap.get(cv2.CAP_PROP_FRAME_COUNT)
        while True:
            while running == False:
                cap.set(cv2.CAP_PROP_POS_FRAMES, start_frame_number)
                ret, frame = cap.read()
                if ret:
                    rgbImage = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                    h, w, ch = rgbImage.shape
                    bytesPerLine = ch * w
                    convertToQtFormat = QImage(rgbImage.data, w, h, bytesPerLine, QImage.Format_RGB888)
                    p = convertToQtFormat.scaled(640, 480, Qt.KeepAspectRatio)
                    self.changePixmap.emit(p)

            while running:
                cap.set(cv2.CAP_PROP_POS_FRAMES, start_frame_number)
                if count == 0:
                    text.append("FPS:")
                    text.append(str(fps))
                    text.append("영상 길이:")
                    text.append(str(frame_count/fps))

                ret, frame = cap.read()
                if ret:
                    rgbImage = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                    h, w, ch = rgbImage.shape
                    bytesPerLine = ch * w
                    convertToQtFormat = QImage(rgbImage.data, w, h, bytesPerLine, QImage.Format_RGB888)
                    p = convertToQtFormat.scaled(640, 480, Qt.KeepAspectRatio)
                    self.changePixmap.emit(p)
                count += 1
                start_frame_number += 1

class MainWidget(QWidget):
    def __init__(self):
        super().__init__()
        btn1 = QPushButton("파일 선택")
        btn1.clicked.connect(self.file_select)
        btn1.setCheckable(True)
        self.label = QLabel(self)
        global text
        self.text = QTextBrowser(self)
        text = self.text

        btn2 = QPushButton("파일 전송")
        btn2.clicked.connect(self.file_upload)
        btn2.setCheckable(True)

        btn3 = QPushButton("비디오 시작")
        btn3.clicked.connect(self.clicked_play)
        
        btn4 = QPushButton("비디오 정지")
        btn4.clicked.connect(self.clicked_stop)

        btn5 = QPushButton(">>")
        btn5.clicked.connect(self.clicked_forward)

        btn6 = QPushButton("<<")
        btn6.clicked.connect(self.clicked_backward)

        vbox = QVBoxLayout()
        vbox.addWidget(btn1)
        vbox.addWidget(btn2)
        vbox.addWidget(btn3)
        vbox.addWidget(btn4)
        vbox.addWidget(btn5)
        vbox.addWidget(btn6)
        vbox.addWidget(self.label)
        vbox.addWidget(self.text)

        self.setLayout(vbox)
        self.setWindowTitle('File Button')
        self.setGeometry(500,500,700,600)

    def file_upload(self):
        x1 = Thread1(self)
        x1.start()
    
    @pyqtSlot(QImage)
    def setImage(self, image):
        self.label.setPixmap(QPixmap.fromImage(image))

    def file_select(self):
        global fname, x2
        fname = QFileDialog.getOpenFileName(self)
        file_name, ext = os.path.splitext(fname[0])

        if ext in ['.mp4']:
            self.text.append("파일 경로:")
            self.text.append(fname[0])
            x2 = Thread2(self)
            x2.changePixmap.connect(self.setImage)
            x2.start()
            self.show()
        else:
            self.text.setText("동영상 파일이 아닙니다.")
    
    def clicked_play(self):
        global running, x2
        running = True
        x2.start()
        print("start video")

    def clicked_stop(self):
        global running
        running = False
        print("stop video")
    
    def clicked_forward(self):
        global start_frame_number
        start_frame_number += 50
        print("앞으로")

    def clicked_backward(self):
        global start_frame_number
        start_frame_number -= 50
        if start_frame_number <= 0: start_frame_number = 0
        print("뒤로")

if __name__ == '__main__':
    running = False
    global count, start_frame_number
    count = 0
    start_frame_number = 0
    app = QApplication(sys.argv)
    widget = MainWidget()
    widget.show()
    sys.exit(app.exec_())