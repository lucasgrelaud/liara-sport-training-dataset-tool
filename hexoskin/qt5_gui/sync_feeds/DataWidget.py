import numpy

from PyQt5.QtCore import QDir

from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtWidgets import QStyle
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtWidgets import QHBoxLayout
from PyQt5.QtWidgets import QVBoxLayout

from pyqtgraph import PlotWidget


class DataWidget(QWidget):
    def __init__(self, parent, shared_data):
        super(DataWidget, self).__init__(parent)
        self.shared_data = shared_data

        # Add the file selection controls
        self.dir_picker_button = QPushButton()
        self.dir_picker_button.setEnabled(True)
        self.dir_picker_button.setIcon(self.style().standardIcon(QStyle.SP_DirIcon))
        self.dir_picker_button.setToolTip('Select the directory using the file explorer')
        self.dir_picker_button.clicked.connect(self.open_dir_picker)

        self.dir_path_input = QLineEdit()
        self.dir_path_input.setPlaceholderText('Path to hexoskin data directory.')
        self.dir_path_input.textEdited.connect(self.manual_file_definition)

        self.load_dir_button = QPushButton('Load clip')
        self.load_dir_button.setEnabled(False)
        self.load_dir_button.clicked.connect(self.load_file)

        dir_layout = QHBoxLayout()
        dir_layout.setContentsMargins(0, 0, 0, 0)
        dir_layout.addWidget(self.dir_picker_button)
        dir_layout.addWidget(self.dir_path_input)
        dir_layout.addWidget(self.load_dir_button)

        self.plot_widget = PlotWidget()

        self.v_box = QVBoxLayout()
        self.v_box.addLayout(dir_layout)
        self.v_box.addWidget(self.plot_widget)

        self.setLayout(self.v_box)

    def open_dir_picker(self):
        self.shared_data.data_dir = QFileDialog.getExistingDirectory(self, 'Open the Hexoskin data directory',
                                                                     QDir.homePath())
        if self.shared_data.data_dir != '':
            self.dir_path_input.setText(self.shared_data.data_dir)
            self.load_dir_button.setEnabled(True)

    def manual_file_definition(self):
        if self.dir_path_input.text() != '':
            self.shared_data.data_dir = self.dir_path_input.text()
            self.load_dir_button.setEnabled(True)

    def load_file(self):
        if self.shared_data.data_dir != '':

