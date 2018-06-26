from PyQt5.QtCore import QDir

from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtWidgets import QVBoxLayout
from PyQt5.QtWidgets import QHBoxLayout
from PyQt5.QtWidgets import QStyle
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtWidgets import QMessageBox


from data_handling import export_dataset

class ExportActionWidget(QWidget):

    def __init__(self, parent, shared_data):
        super(ExportActionWidget, self).__init__(parent)
        self.shared_data = shared_data

        # Create the elements to select the output path
        self.dir_picker_button = QPushButton()
        self.dir_picker_button.setText("Select output directory")
        self.dir_picker_button.setIcon(self.style().standardIcon(QStyle.SP_DirIcon))
        self.dir_picker_button.setToolTip('Select the directory using the file explorer')
        self.dir_picker_button.clicked.connect(self.open_export_dir)
        if self.shared_data.parameter is None:
            self.dir_picker_button.setEnabled(False)

        self.dir_picker_path = QLineEdit()
        self.dir_picker_path.setPlaceholderText('Path to the output directory')
        self.dir_picker_path.setReadOnly(True)

        # Create the export buttons
        self.export_separated_button = QPushButton()
        self.export_separated_button.setText('Export to separated files')
        self.export_separated_button.setEnabled(False)

        self.export_dataset_button = QPushButton()
        self.export_dataset_button.setText("Export to dataset")
        self.export_dataset_button.clicked.connect(self.export_dataset_action)
        self.export_dataset_button.setEnabled(False)

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

    def open_export_dir(self):
        self.shared_data.output_dir = QFileDialog.getExistingDirectory(self, 'Open the output directory', QDir.homePath())
        self.dir_picker_path.setText(self.shared_data.output_dir)
        self.export_dataset_button.setEnabled(True)

    def export_dataset_action(self):
        export_dataset(self.shared_data.parameter, self.shared_data.parameter_export_list, self.shared_data.output_dir)
        QMessageBox.information(self, 'Dataset exported',
                                'The dataset has been exported and is accessible in the selected directory')

