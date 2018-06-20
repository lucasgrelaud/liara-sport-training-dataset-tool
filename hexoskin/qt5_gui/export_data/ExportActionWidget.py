from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtWidgets import QVBoxLayout
from PyQt5.QtWidgets import QHBoxLayout
from PyQt5.QtWidgets import QStyle

class ExportActionWidget(QWidget):

    def __init__(self, parent, shared_data):
        super(ExportActionWidget, self).__init__(parent)
        self.shared_data = shared_data

        # Create the elements to select the output path
        self.dir_picker_button = QPushButton()
        self.dir_picker_button.setEnabled(True)
        self.dir_picker_button.setText("Select output directory")
        self.dir_picker_button.setIcon(self.style().standardIcon(QStyle.SP_DirIcon))
        self.dir_picker_button.setToolTip('Select the directory using the file explorer')

        self.dir_picker_path = QLineEdit()
        self.dir_picker_path.setPlaceholderText('Path to the output directory')
        self.dir_picker_path.setReadOnly(True)

        # Create the export buttons
        self.export_separated_button = QPushButton()
        self.export_separated_button.setText('Export to separated files')

        self.export_dataset_button = QPushButton()
        self.export_dataset_button.setText("Export to dataset")

        dir_picker_layout = QHBoxLayout()
        dir_picker_layout.addWidget(self.dir_picker_button)
        dir_picker_layout.addWidget(self.dir_picker_path)

        export_button_layout = QHBoxLayout()
        export_button_layout.addStretch(1)
        export_button_layout.addWidget(self.export_separated_button)
        export_button_layout.addStretch(1)
        export_button_layout.addWidget(self.export_dataset_button)
        export_button_layout.addStretch(1)

        main_layout = QVBoxLayout()
        main_layout.addLayout(dir_picker_layout)
        main_layout.addSpacing(15)
        main_layout.addLayout(export_button_layout)
        main_layout.addStretch(1)

        self.setLayout(main_layout)
