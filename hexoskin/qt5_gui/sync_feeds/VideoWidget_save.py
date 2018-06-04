from PyQt5.QtCore import Qt
from PyQt5.QtCore import QDir
from PyQt5.QtCore import QUrl
from PyQt5.QtCore import QTime

from PyQt5.QtGui import QPixmap
from PyQt5.QtGui import QMatrix2x2

from PyQt5.QtMultimedia import QMediaContent
from PyQt5.QtMultimedia import QMediaPlayer

from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QSlider
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtWidgets import QComboBox
from PyQt5.QtWidgets import QStyle
from PyQt5.QtWidgets import QSizePolicy
from PyQt5.QtWidgets import QHBoxLayout
from PyQt5.QtWidgets import QVBoxLayout


from PyQt5.QtMultimediaWidgets import QVideoWidget

from hexoskin.qt5_gui.app_config import get_tags_list


class VideoWidget(QWidget):

    def __init__(self, parent, shared_data):
        super(VideoWidget, self).__init__(parent)
        self.shared_data = shared_data
        self.shared_data.video_sync = 'HH:SS:MM:zzz'
        self.shared_data.update_sync.emit()

        # Add the object and data attributes.
        self.media_player = QMediaPlayer(None, QMediaPlayer.VideoSurface)

        # Add the video player
        self.video_player = QVideoWidget()

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

        self.time_code = QLabel()
        self.time_code.setText('HH:SS:MM:zzz / HH:SS:MM:zzz')

        self.sync_button = QPushButton()
        self.sync_button.setEnabled(False)
        self.sync_button.setText('Set sync time')
        self.sync_button.clicked.connect(self.sync_video)

        self.error_label = QLabel()
        self.error_label.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Maximum)

        # Add the tags controls
        self.tags_combobox = QComboBox()
        self.tags_combobox.setEnabled(False)
        self.tags_combobox.addItems(get_tags_list())

        self.tags_button = QPushButton()
        self.tags_button.setEnabled(False)
        self.tags_button.setText('Add the selected tag')
        self.tags_button.clicked.connect(self.add_tag)

        # Create layouts to place inside widget
        file_layout = QHBoxLayout()
        file_layout.setContentsMargins(0, 0, 0, 0)
        file_layout.addWidget(self.file_picker_button)
        file_layout.addWidget(self.file_path_input)
        file_layout.addWidget(self.load_file_button)

        control_layout = QHBoxLayout()
        control_layout.setContentsMargins(0, 0, 0, 0)
        control_layout.addWidget(self.play_button)
        control_layout.addWidget(self.sync_button)
        control_layout.addWidget(self.position_slider)
        control_layout.addWidget(self.time_code)

        tags_layout = QHBoxLayout()
        tags_layout.setContentsMargins(0, 0, 0, 0)
        tags_layout.addWidget(self.tags_combobox)
        tags_layout.addWidget(self.tags_button)
        tags_layout.addStretch(1)

        layout = QVBoxLayout()
        layout.addLayout(file_layout)
        layout.addWidget(self.video_player)
        layout.addLayout(control_layout)
        layout.addLayout(tags_layout)
        layout.addWidget(self.error_label)

        # Set widget to contain window contents
        self.setLayout(layout)

        self.media_player.setVideoOutput(self.video_player)
        self.media_player.stateChanged.connect(self.media_state_changed)
        self.media_player.positionChanged.connect(self.position_changed)
        self.media_player.durationChanged.connect(self.duration_changed)
        self.media_player.error.connect(self.handle_error)

    def open_file_picker(self):
        self.shared_data.video_path, _ = QFileDialog.getOpenFileName(self, "Open video clip", QDir.homePath())
        if self.shared_data.video_path != '':
            self.file_path_input.setText(self.shared_data.video_path)
            self.load_file_button.setEnabled(True)

    def manual_file_definition(self):
        if self.file_path_input.text() != '':
            self.shared_data.video_path = self.file_path_input.text()
            self.load_file_button.setEnabled(True)

    def load_file(self):
        if self.shared_data.video_path != '':
            self.media_player.setMedia(
                QMediaContent(QUrl.fromLocalFile(self.shared_data.video_path)))
            self.play_button.setEnabled(True)
            self.sync_button.setEnabled(True)
            self.tags_button.setEnabled(True)
            self.tags_combobox.setEnabled(True)

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
        self.update_time_code(position)

    def duration_changed(self, duration):
        self.position_slider.setRange(0, duration)

    def set_position(self, position):
        self.media_player.setPosition(position)

    def handle_error(self):
        self.play_button.setEnabled(False)
        self.error_label.setText("Error: " + self.media_player.errorString())

    def update_time_code(self, current_position):
        time_string = ''
        current_position /= 1000
        if current_position and self.media_player.duration():
            duration = self.media_player.duration() / 1000
            current_time = QTime(int((current_position / 3600) % 60), int((current_position / 60) % 60),
                                 int(current_position % 60), int((current_position * 1000) % 1000))
            total_time = QTime(int((duration / 3600) % 60), int((duration / 60) % 60), int(duration % 60),
                               int((duration * 1000) % 1000))
            time_string = '{} / {}'.format(current_time.toString("HH:mm:ss:zzz"), total_time.toString("HH:mm:ss:zzz"))
            self.time_code.setText(time_string)

    def sync_video(self):
        self.shared_data.video_sync = self.time_code.text().split(' ')[0]
        self.shared_data.update_sync.emit()

    def add_tag(self):
        self.shared_data.tags[self.time_code.text().split(' ')[0]] = self.tags_combobox.currentText()
        self.shared_data.update_tags.emit('add')


