from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QHBoxLayout
from PyQt5.QtWidgets import QVBoxLayout

from .DatasetDisplayWidget import DatasetDisplayWidget
from .ExportSelectorWidget import ExportSelectorWidget
from .ExportActionWidget import ExportActionWidget

class ExportationInterface(QWidget):
    def __init__(self, parent, shared_data):
        super(ExportationInterface, self).__init__(parent)
        self.shared_data = shared_data

        self.dataset_display_widget = DatasetDisplayWidget(self, self.shared_data)
        self.export_select_widget = ExportSelectorWidget(self, self.shared_data)
        self.export_action_widget = ExportActionWidget(self, self.shared_data)

        right_layout = QVBoxLayout()
        main_layout = QHBoxLayout()

        right_layout.addWidget(self.export_select_widget)
        right_layout.addSpacing(15)
        right_layout.addWidget(self.export_action_widget)
        right_layout.addStretch(1)

        main_layout.addWidget(self.dataset_display_widget)
        main_layout.addLayout(right_layout)

        self.setLayout(main_layout)