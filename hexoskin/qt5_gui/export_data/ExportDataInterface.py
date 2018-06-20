from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QHBoxLayout
from PyQt5.QtWidgets import QVBoxLayout

from .TagDisplayWidget import TagDisplayWidget
from .ExportSelectorWidget import ExportSelectorWidget
from .ExportActionWidget import ExportActionWidget

class ExportDataInterface(QWidget):
    def __init__(self, parent, shared_data):
        super(ExportDataInterface, self).__init__(parent)
        self.shared_data = shared_data

        self.tag_display_widget = TagDisplayWidget(self, self.shared_data)
        self.export_select_widget = ExportSelectorWidget(self, self.shared_data)
        self.export_action_widget = ExportActionWidget(self, self.shared_data)

        main_layout = QVBoxLayout()
        h_box_layout = QHBoxLayout()

        main_layout.addWidget(self.export_select_widget)
        main_layout.addSpacing(15)
        main_layout.addWidget(self.export_action_widget)
        main_layout.addStretch(1)

        h_box_layout.addWidget(self.tag_display_widget)
        h_box_layout.addLayout(main_layout)

        self.setLayout(h_box_layout)