from PyQt5.QtWidgets import QHBoxLayout
from PyQt5.QtWidgets import QVBoxLayout
from PyQt5.QtWidgets import QWidget

from .DatasetDisplayWidget import DatasetDisplayWidget
from .ExportActionWidget import ExportActionWidget
from .ExportSelectorWidget import ExportSelectorWidget


class ExportationInterface(QWidget):
    def __init__(self, parent, shared_data):
        super(ExportationInterface, self).__init__(parent)
        self.__shared_data = shared_data

        self.__dataset_display_widget = DatasetDisplayWidget(self, self.__shared_data)
        self.__export_select_widget = ExportSelectorWidget(self, self.__shared_data)
        self.__export_action_widget = ExportActionWidget(self, self.__shared_data)

        right_layout = QVBoxLayout()
        main_layout = QHBoxLayout()

        right_layout.addWidget(self.__export_select_widget)
        right_layout.addSpacing(15)
        right_layout.addWidget(self.__export_action_widget)
        right_layout.addStretch(1)

        main_layout.addWidget(self.__dataset_display_widget)
        main_layout.addLayout(right_layout)

        self.setLayout(main_layout)
