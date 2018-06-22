from PyQt5.QtCore import Qt
from PyQt5.QtCore import QStandardPaths
from PyQt5.QtCore import QTime
from PyQt5.QtCore import pyqtSignal

from PyQt5.QtGui import QTransform

from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QGraphicsScene
from PyQt5.QtWidgets import QGraphicsView
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QSlider
from PyQt5.QtWidgets import QDialog
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtWidgets import QStyle
from PyQt5.QtWidgets import QHBoxLayout
from PyQt5.QtWidgets import QVBoxLayout

from PyQt5.QtMultimedia import QMediaPlayer
from PyQt5.QtMultimedia import QMediaContent
from PyQt5.QtMultimediaWidgets import QGraphicsVideoItem


class VideoPlayerWidget(QWidget):

    error = pyqtSignal(str)
    file_loaded = pyqtSignal()

    def __init__(self, parent, shared_data):
        super(VideoPlayerWidget, self).__init__(parent)
        self.shared_data = shared_data
        # Create the video elements
        self.__media_player = QMediaPlayer(self, QMediaPlayer.VideoSurface)
        self.__video_item = QGraphicsVideoItem()
        self.__scene = QGraphicsScene(self)
        self.__graphic_view = QGraphicsView(self.__scene)
        self.__rotation = 0
        self.__video_duration = None

        self.__scene.addItem(self.__video_item)

        # Create the video controls
        self.__size_label = QLabel()
        self.__size_label.setText('Set size : ')

        self.__size_slider = QSlider(Qt.Horizontal)
        self.__size_slider.setRange(50,150)
        self.__size_slider.setValue(100)
        self.__size_slider.setFixedWidth(150)
        self.__size_slider.setEnabled(False)
        self.__size_slider.sliderMoved.connect(self.__set_size)

        self.__rotate_left_button = QPushButton()
        self.__rotate_left_button.setText("Rotate left")
        self.__rotate_left_button.setToolTip("Rotate the video 90° to the left.")
        self.__rotate_left_button.setEnabled(False)
        self.__rotate_left_button.clicked.connect(self.__rotate_video_left)

        self.__rotate_right_button = QPushButton()
        self.__rotate_right_button.setText("Rotate right")
        self.__rotate_right_button.setToolTip("Rotate the video 90° to the right.")
        self.__rotate_right_button.setEnabled(False)
        self.__rotate_right_button.clicked.connect(self.__rotate_video_right)

        self.__open_video_button = QPushButton()
        self.__open_video_button.setText("Open video")
        self.__open_video_button.setIcon(self.style().standardIcon(QStyle.SP_DriveCDIcon))
        self.__open_video_button.setToolTip("Select and load the video clip.")
        self.__open_video_button.clicked.connect(self.__open_file)

        self.__play_button = QPushButton()
        self.__play_button.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))
        self.__play_button.setToolTip("Play the video.")
        self.__play_button.setEnabled(False)
        self.__play_button.clicked.connect(self.__play)

        self.__stop_button = QPushButton()
        self.__stop_button.setIcon(self.style().standardIcon(QStyle.SP_MediaStop))
        self.__stop_button.setToolTip("Stop the video.")
        self.__stop_button.setEnabled(False)
        self.__stop_button.clicked.connect(self.__stop)

        self.__video_slider = QSlider(Qt.Horizontal)
        self.__video_slider.setRange(0, 0)
        self.__video_slider.sliderMoved.connect(self.__set_position)

        self.__time_code = QLabel()
        self.__time_code.setText('HH:SS:MM:zzz / HH:SS:MM:zzz')

        # Create the layouts
        top_control_layout = QHBoxLayout()
        top_control_layout.setContentsMargins(0, 0, 0, 0)
        top_control_layout.addWidget(self.__open_video_button)
        top_control_layout.addStretch(1)
        top_control_layout.addWidget(self.__size_label)
        top_control_layout.addWidget(self.__size_slider)
        top_control_layout.addWidget(self.__rotate_left_button)
        top_control_layout.addWidget(self.__rotate_right_button)

        bottom_control_layout = QHBoxLayout()
        bottom_control_layout.setContentsMargins(0, 0, 0, 0)
        bottom_control_layout.addWidget(self.__play_button)
        bottom_control_layout.addWidget(self.__stop_button)
        bottom_control_layout.addWidget(self.__video_slider)
        bottom_control_layout.addWidget(self.__time_code)

        widget_layout = QVBoxLayout()
        widget_layout.addLayout(top_control_layout)
        widget_layout.addWidget(self.__graphic_view)
        widget_layout.addLayout(bottom_control_layout)

        # Configure the video player
        self.__media_player.setVideoOutput(self.__video_item)
        self.__media_player.stateChanged.connect(self.__media_state_changed)
        self.__media_player.positionChanged.connect(self.__position_changed)
        self.__media_player.durationChanged.connect(self.__duration_changed)
        self.__media_player.error.connect(self.handle_error)

        # Set the widget layout
        self.setLayout(widget_layout)

    def __open_file(self):
        file_dialog = QFileDialog(self)
        file_dialog.setAcceptMode(QFileDialog.AcceptOpen)
        file_dialog.setWindowTitle("Open a video clip")
        file_dialog.setFileMode(QFileDialog.ExistingFile)
        file_dialog.setDirectory(QStandardPaths.standardLocations(QStandardPaths.MoviesLocation)[0])
        if file_dialog.exec() == QDialog.Accepted:
            self.shared_data.video_path = file_dialog.selectedUrls()[0]
            try:
                self.load_video(file_dialog.selectedUrls()[0])
                self.__open_video_button.setEnabled(False)
            except TypeError:
                pass

    def load_video(self, url):
        self.__media_player.setMedia(QMediaContent(url))
        self.__play_button.setEnabled(True)
        self.__stop_button.setEnabled(True)
        self.__rotate_left_button.setEnabled(True)
        self.__rotate_right_button.setEnabled(True)
        self.__size_slider.setEnabled(True)
        self.__update_time_code(0)
        self.file_loaded.emit()

    def __play(self):
        if self.__media_player.state() == QMediaPlayer.PlayingState:
            self.__media_player.pause()
        else:
            self.__media_player.play()

    def __stop(self):
        self.__media_player.stop()

    def __media_state_changed(self, state):
        if state == QMediaPlayer.PlayingState:
            self.__play_button.setIcon(self.style().standardIcon(QStyle.SP_MediaPause))
            self.__play_button.setToolTip("Pause the video.")
        else:
            self.__play_button.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))
            self.__play_button.setToolTip("Play the video.")

    def __set_position(self, position):
        self.__media_player.setPosition(position)

    def __position_changed(self, position):
        self.__video_slider.setValue(position)
        self.__update_time_code(position)

    def __duration_changed(self, duration):
        self.__video_slider.setRange(0, duration)
        self.__video_duration = QTime(int((duration / 3600) % 60), int((duration / 60) % 60), int(duration % 60),
                                      int((duration * 1000) % 1000))

    def __update_time_code(self, current_position):
        time_string = ''
        current_position /= 1000
        if current_position and self.__media_player.duration():
            duration = self.__media_player.duration() / 1000
            current_time = QTime(int((current_position / 3600) % 60), int((current_position / 60) % 60),
                                 int(current_position % 60), int((current_position * 1000) % 1000))

            time_string = '{} / {}'.format(current_time.toString("HH:mm:ss:zzz"),
                                           self.__video_duration.toString("HH:mm:ss:zzz"))
            self.__time_code.setText(time_string)

    def __rotate_video_left(self):
        if self.__rotation != 270:
            self.__rotation += 90
        else:
            self.__rotation = 0

        x = self.__video_item.boundingRect().width() / 2
        y = self.__video_item.boundingRect().height() / 2
        self.__video_item.setTransform(QTransform().translate(x, y).rotate(self.__rotation).translate(-x, -y))

    def __rotate_video_right(self):
        if self.__rotation != -270:
            self.__rotation -= 90
        else:
            self.__rotation = 0

        x = self.__video_item.boundingRect().width() / 2
        y = self.__video_item.boundingRect().height() / 2
        self.__video_item.setTransform(QTransform().translate(x, y).rotate(self.__rotation).translate(-x, -y))

    def __set_size(self, percent):
        scale = percent / 100
        self.__video_item.setScale(scale)

    def handle_error(self, error):
        pass

    def current_timecode(self):
        return self.__time_code.text().split(' ')[0]