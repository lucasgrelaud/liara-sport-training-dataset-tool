from _ruamel_yaml import YAMLError

from datetime import datetime

from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QComboBox
from PyQt5.QtWidgets import QHBoxLayout
from PyQt5.QtWidgets import QVBoxLayout

from hexoskin.qt5_gui.app_config import get_tags_list

from .VideoPlayerWidget import VideoPlayerWidget

class VideoWidget(QWidget):

    def __init__(self, parent, shared_data):
        super(VideoWidget, self).__init__(parent)
        self.shared_data = shared_data
        self.shared_data.update_sync.connect(self.update_sync)

        # Add the video player
        self.video_player = VideoPlayerWidget(self)
        self.video_player.error.connect(self.handle_error)
        self.video_player.file_loaded.connect(self.file_loaded)

        # Create the sync control
        self.video_sync_button = QPushButton()
        self.video_sync_button.setText("Sync Video")
        self.video_sync_button.setToolTip("Set the sync timecode of the video.")
        self.video_sync_button.setEnabled(False)
        self.video_sync_button.clicked.connect(self.video_sync)

        # Create the tags controls
        self.tags_combobox = QComboBox()
        self.tags_combobox.setEnabled(False)
        try:
            self.tags_combobox.addItems(get_tags_list())
        except YAMLError as error:
            self.handle_error(error)

        self.tags_button = QPushButton()
        self.tags_button.setText("Add tag")
        self.tags_button.setToolTip("Add a tag to the list using the current timecode and selected tag in the list.")
        self.tags_button.setEnabled(False)
        self.tags_button.clicked.connect(self.add_tag)

        self.tags_other_button = QPushButton()
        self.tags_other_button.setText("Add 'Other' tag")
        self.tags_other_button.setToolTip("Add a 'Other' tag to the list using the current timecode.")
        self.tags_other_button.setEnabled(False)
        self.tags_other_button.clicked.connect(self.add_other_tag)

        # Create the layouts
        bottom_control_layout = QHBoxLayout()
        bottom_control_layout.addWidget(self.tags_combobox)
        bottom_control_layout.addWidget(self.tags_button)
        bottom_control_layout.addWidget(self.tags_other_button)
        bottom_control_layout.addStretch(1)
        bottom_control_layout.addWidget(self.video_sync_button)

        widget_layout = QVBoxLayout()
        widget_layout.addWidget(self.video_player)
        widget_layout.addLayout(bottom_control_layout)

        self.setLayout(widget_layout)

    def handle_error(self, error):
        print(error)

    def file_loaded(self):
        self.video_sync_button.setEnabled(True)
        self.shared_data.video_sync = 'HH:SS:MM:zzz'
        self.shared_data.update_sync.emit()

    def video_sync(self):
        self.shared_data.video_sync = self.video_player.current_timecode()
        self.shared_data.update_sync.emit()

    def update_sync(self):
        if self.shared_data.video_sync != 'HH:SS:MM:zzz' and self.shared_data.data_sync != 'HH:SS:MM:zzz':
            self.tags_combobox.setEnabled(True)
            self.tags_button.setEnabled(True)
            self.tags_other_button.setEnabled(True)
        else:
            self.tags_combobox.setEnabled(False)
            self.tags_button.setEnabled(False)
            self.tags_other_button.setEnabled(False)

    def add_tag(self):
        video_sync_array = self.shared_data.video_sync.split(':')
        data_sync_array = self.shared_data.data_sync.split(':')
        video_time = datetime(1970, 1, 1, int(video_sync_array[0]), int(video_sync_array[1]), int(video_sync_array[2]),
                              int(video_sync_array[3]) * 1000)
        data_time = datetime(1970, 1, 1, int(data_sync_array[0]), int(data_sync_array[1]), int(data_sync_array[2]),
                             int(data_sync_array[3]) * 1000)
        time_delta = video_time - data_time

        timecode_array = self.video_player.current_timecode().split(":")
        timecode = datetime(1970, 1, 1, int(timecode_array[0]), int(timecode_array[1]), int(timecode_array[2]),
                            int(timecode_array[3]) * 1000)
        timecode += time_delta
        self.shared_data.update_tags.emit('add', timecode.strftime('%H:%M:%S:') + str(int(timecode.microsecond / 1000)),
                                          self.tags_combobox.currentText())

    def add_other_tag(self):
        video_sync_array = self.shared_data.video_sync.split(':')
        data_sync_array = self.shared_data.data_sync.split(':')
        video_time = datetime(1970, 1, 1, int(video_sync_array[0]), int(video_sync_array[1]), int(video_sync_array[2]),
                              int(video_sync_array[3]) * 1000)
        data_time = datetime(1970, 1, 1, int(data_sync_array[0]), int(data_sync_array[1]), int(data_sync_array[2]),
                             int(data_sync_array[3]) * 1000)
        time_delta = video_time - data_time

        timecode_array = self.video_player.current_timecode().split(":")
        timecode = datetime(1970, 1, 1, int(timecode_array[0]), int(timecode_array[1]), int(timecode_array[2]),
                            int(timecode_array[3]) * 1000)
        timecode += time_delta
        self.shared_data.update_tags.emit('add', timecode.strftime('%H:%M:%S:') + str(int(timecode.microsecond / 1000)),
                                          'Other')
