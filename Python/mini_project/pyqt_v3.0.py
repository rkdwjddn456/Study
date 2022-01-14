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
        res = requests.post('http://192.168.0.103:5000/file_upload', files= upload)

class Thread2(QThread):
    changePixmap = pyqtSignal(QImage)
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
    
    def run(self):
        global running
        cap = cv2.VideoCapture(fname[0])
        fps = cap.get(cv2.CAP_PROP_FPS)
        while running:
            ret, frame = cap.read()
            if ret:
                rgbImage = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                h, w, ch = rgbImage.shape
                bytesPerLine = ch * w
                convertToQtFormat = QImage(rgbImage.data, w, h, bytesPerLine, QImage.Format_RGB888)
                p = convertToQtFormat.scaled(640, 480, Qt.KeepAspectRatio)
                self.changePixmap.emit(p)

class MainWidget(QWidget):
    def __init__(self):
        super().__init__()
        btn1 = QPushButton("파일 선택")
        btn1.clicked.connect(self.file_select)
        btn1.setCheckable(True)
        self.label = QLabel()

        btn2 = QPushButton("파일 전송")
        btn2.clicked.connect(self.file_upload)
        btn2.setCheckable(True)

        btn3 = QPushButton("비디오 시작")
        btn3.clicked.connect(self.clicked_play)
        
        btn4 = QPushButton("비디오 정지")
        btn4.clicked.connect(self.clicked_stop)

        vbox = QVBoxLayout()
        vbox.addWidget(btn1)
        vbox.addWidget(btn2)
        vbox.addWidget(btn3)
        vbox.addWidget(btn4)
        vbox.addWidget(self.label)

        self.setLayout(vbox)
        self.setWindowTitle('File Button')
        self.setGeometry(300,300,300,200)

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
            self.label.setText(fname[0])
            x2 = Thread2(self)
            x2.changePixmap.connect(self.setImage)
            x2.start()
            self.show()
        else:
            self.label.setText("동영상 파일이 아닙니다.")
    
    def clicked_play(self):
        global running, x2
        running = True
        x2.start()
        print("start video")

    def clicked_stop(self):
        global running
        running = False
        print("stop video")

if __name__ == '__main__':
    running = False
    app = QApplication(sys.argv)
    widget = MainWidget()
    widget.show()
    sys.exit(app.exec_())