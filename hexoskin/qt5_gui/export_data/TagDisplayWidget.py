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
        self.tags_label = QLabel()
        self.tags_label.setText('Tags list')

        self.tags_table = QTableWidget()
        self.tags_table.setRowCount(1)
        self.tags_table.setColumnCount(2)
        self.tags_table.setHorizontalHeaderItem(0, QTableWidgetItem('TimeCode'))
        self.tags_table.setHorizontalHeaderItem(1, QTableWidgetItem('Tag'))
        self.tags_table.verticalHeader().setVisible(True)
        self.tags_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tags_table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.tags_table.setSelectionMode(QAbstractItemView.SingleSelection)
        self.tags_table.setShowGrid(True)
        self.tags_table.setMinimumHeight(500)
        self.tags_table.setMaximumHeight(600)

        main_layout = QVBoxLayout()
        main_layout.addWidget(self.tags_label)
        main_layout.addWidget(self.tags_table)
        main_layout.addStretch(1)

        self.setLayout(main_layout)

        self.fill_table()

    def fill_table(self):
        if len(self.shared_data.tags) != 0:
            for key, value in self.shared_data.tags.items():
                self.tags_table.setItem(self.tags_table.rowCount() - 1, 0, QTableWidgetItem(key))
                self.tags_table.setItem(self.tags_table.rowCount() - 1, 1, QTableWidgetItem(value))
                self.tags_table.insertRow(self.tags_table.rowCount())