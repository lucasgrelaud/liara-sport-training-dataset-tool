from PyQt5.QtCore import QObject
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtCore import QDir

from hexoskin.standardize.breathing import Breathing
from hexoskin.standardize.cardiology import Cardiology
from hexoskin.standardize.moves import Moves

class SharedData(QObject):
    update = pyqtSignal()

    def __init__(self):
        QObject.__init__(self)
        self.video_path = None
        self.video_sync = None

        self.data_dir = None
        self.data_sync = None

        self.breathing = None
        self.cardiology = None
        self.moves = None

    def init_data(self):
        self.breathing = Breathing(self.data_dir, QDir.tempPath())
        self.cardiology = Cardiology(self.data_dir, QDir.tempPath())
        self.moves = Moves(self.data_dir, QDir.tempPath())
