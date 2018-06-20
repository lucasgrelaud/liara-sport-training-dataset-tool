from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QHBoxLayout
from PyQt5.QtWidgets import QVBoxLayout

from .TagDisplayWidget import TagDisplayWidget
from .ExportSelectorWidget import ExportSelectorWidget

class ExportDataInterface(QWidget):
    def __init__(self, parent, shared_data):
        super(ExportDataInterface, self).__init__(parent)
        self.shared_data = shared_data

        self.tag_display_widget = TagDisplayWidget(self, self.shared_data)
        self.export_data_widget = ExportSelectorWidget(self, self.shared_data)

        main_layout = QVBoxLayout()
        h_box_layout = QHBoxLayout()

        main_layout.addWidget(self.export_data_widget)

        h_box_layout.addWidget(self.tag_display_widget)
        h_box_layout.addLayout(main_layout)

        self.setLayout(h_box_layout)