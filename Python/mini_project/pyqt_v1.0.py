import sys
import requests
from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5.QtCore import *

class Thread1(QThread):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
    
    def run(self):
        files = open(fname[0], 'rb')
        upload = {'file': files}
        res = requests.post('http://192.168.0.103:5000/file_upload', files= upload)

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

        vbox = QVBoxLayout()
        vbox.addWidget(btn1)
        vbox.addWidget(btn2)
        vbox.addWidget(self.label)

        self.setLayout(vbox)
        self.setWindowTitle('File Button')
        self.setGeometry(300,300,300,200)

    def file_upload(self):
        x1 = Thread1(self)
        x1.start()

    def file_select(self):
        global fname
        fname = QFileDialog.getOpenFileName(self)
        self.label.setText(fname[0])

if __name__ == '__main__':
    app = QApplication(sys.argv)
    widget = MainWidget()
    widget.show()
    sys.exit(app.exec_())