from PyQt5.QtCore import QObject
from PyQt5.QtCore import pyqtSignal


class SharedData(QObject):
    update = pyqtSignal()

    def __init__(self):
        QObject.__init__(self)
        self.video_sync = None
        self.data_start_sync = None
