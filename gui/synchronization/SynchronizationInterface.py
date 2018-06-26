from PyQt5.QtWidgets import QHBoxLayout
from PyQt5.QtWidgets import QVBoxLayout
from PyQt5.QtWidgets import QWidget

from .DataWidget import DataWidget
from .SideBarWidget import SideBarWidget
from .VideoWidget import VideoWidget


class SynchronizationInterface(QWidget):
    def __init__(self, parent, shared_data):
        super(SynchronizationInterface, self).__init__(parent)
        self.__shared_data = shared_data

        # Create the widgets
        self.__video_widget = VideoWidget(self, self.__shared_data)
        self.__data_widget = DataWidget(self, self.__shared_data)
        self.__sidebar_widget = SideBarWidget(self, self.__shared_data)

        # Create the layouts
        self.__left_layout = QVBoxLayout()
        self.__left_layout.addWidget(self.__video_widget)
        self.__left_layout.addWidget(self.__data_widget)
        self.__left_layout.setStretchFactor(self.__video_widget, 2)
        self.__left_layout.setStretchFactor(self.__data_widget, 1)

        self.__main_layout = QHBoxLayout()
        self.__main_layout.addLayout(self.__left_layout)
        self.__main_layout.addWidget(self.__sidebar_widget)
        self.__main_layout.setStretchFactor(self.__left_layout, 3)
        self.__main_layout.setStretchFactor(self.__sidebar_widget, 1)

        # Set the layout
        self.setLayout(self.__main_layout)
