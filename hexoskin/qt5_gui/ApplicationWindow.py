import sys
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QVBoxLayout
from PyQt5.QtWidgets import QHBoxLayout
from .VideoWidget import VideoWidget


class ApplicationWindow(QMainWindow):
    def __init__(self, parent=None):
        super(ApplicationWindow, self).__init__(parent)
        self.title = 'Hexoskin Analysis Tool'
        self.left = 0
        self.top = 0
        self.width = 1600
        self.height = 1200
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.create_layout()
        self.show()

    def create_layout(self):
        video_widget = VideoWidget(self)
        self.setCentralWidget(video_widget)
