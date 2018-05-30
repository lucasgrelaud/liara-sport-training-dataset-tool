from PyQt5.QtCore import QObject
from PyQt5.QtCore import pyqtSignal

from hexoskin.standardize.breathing import Breathing

class SharedData(QObject):
    update = pyqtSignal()

    def __init__(self):
        QObject.__init__(self)
        self.video_path = None
        self.video_sync = None

        self.data_dir = None
        self.data_start_sync = None

        self.breathing = None
        self.cardiology = None
        self.moves = None

    def init_data(self):
        # self.breathing = Breathing()
