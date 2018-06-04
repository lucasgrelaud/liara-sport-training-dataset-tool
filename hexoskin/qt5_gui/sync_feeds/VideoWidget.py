from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QHBoxLayout
from PyQt5.QtWidgets import QVBoxLayout

from .VideoPlayerWidget import VideoPlayerWidget

class VideoWidget(QWidget):

    def __init__(self, parent, shared_data):
        super(VideoWidget, self).__init__(parent)
        self.shared_data = shared_data
        self.shared_data.video_sync = 'HH:SS:MM:zzz'
        self.shared_data.update_sync.emit()

        # Add the object and data attributes.
        self.video_player = VideoPlayerWidget(self)

        # Add the layouts

        widget_layout = QVBoxLayout()
        widget_layout.addWidget(self.video_player)

        self.setLayout(widget_layout)