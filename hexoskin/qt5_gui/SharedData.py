from PyQt5.QtCore import QObject
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtCore import QDir

from hexoskin.standardize.breathing import Breathing
from hexoskin.standardize.cardiology import Cardiology
from hexoskin.standardize.moves import Moves


class SharedData(QObject):
    update_sync = pyqtSignal()
    update_tags = pyqtSignal(str, str, str)
    tags_updated = pyqtSignal(str, str, str)

    def __init__(self):
        QObject.__init__(self)
        self.video_path = None
        self.video_sync = 'HH:SS:MM:zzz'

        self.data_dir = None
        self.data_sync = 'HH:SS:MM:zzz'

        self.breathing = None
        self.cardiology = None
        self.moves = None

        self.tags = dict()

        self.update_tags.connect(self.update_tags_action)


    def init_data(self):
        self.breathing = Breathing(self.data_dir, QDir.tempPath())
        self.cardiology = Cardiology(self.data_dir, QDir.tempPath())
        self.moves = Moves(self.data_dir, QDir.tempPath())

    def update_tags_action(self, action, timecode, tag):
        if action == 'add':
            tagExist = self.tags.get(timecode)
            self.tags[timecode] = tag
            if tagExist:
                self.tags_updated.emit('update', timecode, tag)
            else:
                self.tags_updated.emit(action, timecode, tag)
        elif action == 'delete':
            del self.tags[timecode]
            self.tags_updated.emit(action, timecode, tag)
