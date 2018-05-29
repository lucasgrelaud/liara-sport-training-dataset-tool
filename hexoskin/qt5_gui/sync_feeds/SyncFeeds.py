from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QHBoxLayout
from PyQt5.QtWidgets import QVBoxLayout

from .VideoWidget import VideoWidget
from .SideBarWidget import SideBarWidget


class SyncFeedsWidget(QWidget):
    def __init__(self, parent, shared_data):
        super(SyncFeedsWidget, self).__init__(parent)
        self.shared_data = shared_data

        self.video_widget = VideoWidget(self, self.shared_data)
        self.side_bar_widget = SideBarWidget(self, self.shared_data)

        self.main = QVBoxLayout()
        self.main.addWidget(self.video_widget)

        self.h_box = QHBoxLayout()
        self.h_box.addLayout(self.main)
        self.h_box.addWidget(self.side_bar_widget)

        self.setLayout(self.h_box)
