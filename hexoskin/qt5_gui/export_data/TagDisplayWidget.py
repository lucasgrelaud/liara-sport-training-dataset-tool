from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QTableWidget
from PyQt5.QtWidgets import QTableWidgetItem
from PyQt5.QtWidgets import QAbstractItemView
from PyQt5.QtWidgets import QVBoxLayout

class TagDisplayWidget(QWidget):

    def __init__(self, parent, shared_data):
        super(TagDisplayWidget, self).__init__(parent)
        self.shared_data = shared_data

        # Create the table
        self.dataset_label = QLabel()
        self.dataset_label.setText('Dataset')
        dataset_font = self.dataset_label.font()
        dataset_font.setBold(True)
        self.dataset_label.setFont(dataset_font)

        self.dataset_table = QTableWidget()
        self.dataset_table.setRowCount(1)
        self.dataset_table.setColumnCount(2)
        self.dataset_table.setHorizontalHeaderItem(0, QTableWidgetItem('TimeCode'))
        self.dataset_table.setHorizontalHeaderItem(1, QTableWidgetItem('Tag'))
        self.dataset_table.verticalHeader().setVisible(True)
        self.dataset_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.dataset_table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.dataset_table.setSelectionMode(QAbstractItemView.SingleSelection)
        self.dataset_table.setShowGrid(True)
        self.dataset_table.setMinimumHeight(500)
        self.dataset_table.setMaximumHeight(600)

        main_layout = QVBoxLayout()
        main_layout.addWidget(self.dataset_label)
        main_layout.addWidget(self.dataset_table)
        main_layout.addStretch(1)

        self.setLayout(main_layout)
