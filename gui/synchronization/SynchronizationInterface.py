from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QVBoxLayout
from PyQt5.QtWidgets import QHBoxLayout

from .VideoWidget import VideoWidget
from .DataWidget import DataWidget
from .SideBarWidget import SideBarWidget

class SynchronizationInterface(QWidget):
        def __init__(self, parent, shared_data):
            super(SynchronizationInterface, self).__init__(parent)
            self.shared_data = shared_data

            self.video_widget = VideoWidget(self, self.shared_data)
            self.data_widget = DataWidget(self, self.shared_data)
            self.sidebar_widget = SideBarWidget(self, self.shared_data)

            self.left_layout = QVBoxLayout()
            self.left_layout.addWidget(self.video_widget)
            self.left_layout.addWidget(self.data_widget)
            self.left_layout.setStretchFactor(self.video_widget, 2)
            self.left_layout.setStretchFactor(self.data_widget, 1)

            self.main_layout = QHBoxLayout()
            self.main_layout.addLayout(self.left_layout)
            self.main_layout.addWidget(self.sidebar_widget)
            self.main_layout.setStretchFactor(self.left_layout, 3)
            self.main_layout.setStretchFactor(self.sidebar_widget, 1)

            self.setLayout(self.main_layout)
