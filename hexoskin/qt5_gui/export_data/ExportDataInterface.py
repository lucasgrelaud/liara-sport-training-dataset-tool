from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QHBoxLayout
from PyQt5.QtWidgets import QVBoxLayout

class ExportDataInterface(QWidget):
    def __init__(self, parent, shared_data):
        super(ExportDataInterface, self).__init__(parent)
        self.shared_data = shared_data

        self.main = QVBoxLayout()
        self.h_box = QHBoxLayout()

        self.setLayout(self.h_box)