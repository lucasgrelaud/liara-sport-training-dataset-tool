import sys

from PyQt5.QtCore import Qt
from PyQt5.QtCore import QDir
from PyQt5.QtCore import QUrl

from PyQt5.QtMultimedia import QMediaContent
from PyQt5.QtMultimedia import QMediaPlayer

from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QSlider
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtWidgets import QStyle
from PyQt5.QtWidgets import QSizePolicy
from PyQt5.QtWidgets import QHBoxLayout
from PyQt5.QtWidgets import QVBoxLayout

from PyQt5.QtMultimediaWidgets import QVideoWidget


class VideoWidget(QWidget):

    def __init__(self, parent):
        super(VideoWidget, self).__init__(parent)

        # Add the object and data attributes.
        self.media_player = QMediaPlayer(None, QMediaPlayer.VideoSurface)
        self.file_path = ''

        # Add the video player
        video_player = QVideoWidget()

        # Add the file selection controls
        self.file_picker_button = QPushButton()
        self.file_picker_button.setEnabled(True)
        self.file_picker_button.setIcon(self.style().standardIcon(QStyle.SP_FileIcon))
        self.file_picker_button.setToolTip('Select the file using the file explorer')
        self.file_picker_button.clicked.connect(self.open_file_picker)

        self.file_path_input = QLineEdit()
        self.file_path_input.setPlaceholderText('Path to the video clip.')
        self.file_path_input.textEdited.connect(self.manual_file_definition)

        self.load_file_button = QPushButton('Load clip')
        self.load_file_button.setEnabled(False)
        self.load_file_button.clicked.connect(self.load_file)


        # Add the video player controls
        self.play_button = QPushButton()
        self.play_button.setEnabled(False)
        self.play_button.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))
        self.play_button.clicked.connect(self.play)

        self.position_slider = QSlider(Qt.Horizontal)
        self.position_slider.setRange(0, 0)
        self.position_slider.sliderMoved.connect(self.set_position)

        self.error_label = QLabel()
        self.error_label.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Maximum)

        # Create layouts to place inside widget
        file_layout = QHBoxLayout()
        file_layout.setContentsMargins(0, 0, 0, 0)
        file_layout.addWidget(self.file_picker_button)
        file_layout.addWidget(self.file_path_input)
        file_layout.addWidget(self.load_file_button)

        control_layout = QHBoxLayout()
        control_layout.setContentsMargins(0, 0, 0, 0)
        control_layout.addWidget(self.play_button)
        control_layout.addWidget(self.position_slider)

        layout = QVBoxLayout()
        layout.addLayout(file_layout)
        layout.addWidget(video_player)
        layout.addLayout(control_layout)
        layout.addWidget(self.error_label)

        # Set widget to contain window contents
        self.setLayout(layout)

        self.media_player.setVideoOutput(video_player)
        self.media_player.stateChanged.connect(self.media_state_changed)
        self.media_player.positionChanged.connect(self.position_changed)
        self.media_player.durationChanged.connect(self.duration_changed)
        self.media_player.error.connect(self.handle_error)

    def open_file_picker(self):
        self.file_path, _ = QFileDialog.getOpenFileName(self, "Open video clip", QDir.homePath())
        if self.file_path != '':
            self.file_path_input.setText(self.file_path)
            self.load_file_button.setEnabled(True)

    def manual_file_definition(self):
        if self.file_path_input.text() != '':
            self.file_path = self.file_path_input.text()
            self.load_file_button.setEnabled(True)

    def load_file(self):
        if self.file_path != '':
            self.media_player.setMedia(
                QMediaContent(QUrl.fromLocalFile(self.file_path)))
            self.play_button.setEnabled(True)

    def play(self):
        if self.media_player.state() == QMediaPlayer.PlayingState:
            self.media_player.pause()
        else:
            self.media_player.play()

    def media_state_changed(self, state):
        if self.media_player.state() == QMediaPlayer.PlayingState:
            self.play_button.setIcon(
                self.style().standardIcon(QStyle.SP_MediaPause))
        else:
            self.play_button.setIcon(
                self.style().standardIcon(QStyle.SP_MediaPlay))

    def position_changed(self, position):
        self.position_slider.setValue(position)

    def duration_changed(self, duration):
        self.position_slider.setRange(0, duration)

    def set_position(self, position):
        self.media_player.set_position(position)

    def handle_error(self):
        self.play_button.setEnabled(False)
        self.error_label.setText("Error: " + self.media_player.errorString())