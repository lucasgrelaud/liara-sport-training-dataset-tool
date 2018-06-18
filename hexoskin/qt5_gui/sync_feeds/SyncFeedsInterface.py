from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QHBoxLayout
from PyQt5.QtWidgets import QVBoxLayout

from .VideoWidget import VideoWidget
from .SideBarWidget import SideBarWidget
from .DataWidget import DataWidget


class SyncFeedsInterface(QWidget):
    def __init__(self, parent, shared_data):
        super().__init__(parent)
        self.shared_data = shared_data

        self.main = QVBoxLayout()
        self.h_box = QHBoxLayout()

        self.video_widget = VideoWidget(self, self.shared_data)
        self.side_bar_widget = SideBarWidget(self, self.shared_data)
        self.data_widget = DataWidget(self, self.shared_data)

        self.main.addWidget(self.video_widget)
        self.main.addWidget(self.data_widget)
        self.main.setStretchFactor(self.video_widget, 1)
        self.main.setStretchFactor(self.data_widget, 1)

        self.h_box.addLayout(self.main)
        self.h_box.addWidget(self.side_bar_widget)
        self.h_box.setStretchFactor(self.main, 3)
        self.h_box.setStretchFactor(self.side_bar_widget, 1)

        self.setLayout(self.h_box)
