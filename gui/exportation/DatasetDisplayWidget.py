from datetime import datetime

from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QTableWidget
from PyQt5.QtWidgets import QTableWidgetItem
from PyQt5.QtWidgets import QAbstractItemView
from PyQt5.QtWidgets import QVBoxLayout

class DatasetDisplayWidget(QWidget):

    def __init__(self, parent, shared_data):
        super(DatasetDisplayWidget, self).__init__(parent)
        self.shared_data = shared_data

        # Create the table
        self.dataset_label = QLabel()
        self.dataset_label.setText('Dataset preview :')
        dataset_font = self.dataset_label.font()
        dataset_font.setBold(True)
        self.dataset_label.setFont(dataset_font)
        self.dataset_table = QTableWidget()
        self.dataset_table.setRowCount(1)
        self.dataset_table.verticalHeader().setVisible(True)
        self.dataset_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.dataset_table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.dataset_table.setSelectionMode(QAbstractItemView.SingleSelection)
        self.dataset_table.setShowGrid(True)
        self.dataset_table.setMinimumHeight(600)

        self.set_columns()
        self.set_row()

        main_layout = QVBoxLayout()
        main_layout.addWidget(self.dataset_label)
        main_layout.addWidget(self.dataset_table)
        main_layout.addStretch(1)

        self.setLayout(main_layout)

        self.shared_data.export_list_updated.connect(self.update_table)

    def set_columns(self):
        self.dataset_table.setColumnCount(1)
        self.dataset_table.setHorizontalHeaderItem(0, QTableWidgetItem('TimeCode'))
        if self.shared_data.parameter_export_list is not None:
            for column_name in self.shared_data.parameter_export_list:
                self.dataset_table.setColumnCount(self.dataset_table.columnCount() + 1)
                self.dataset_table.setHorizontalHeaderItem(self.dataset_table.columnCount() - 1, QTableWidgetItem(column_name))
        self.dataset_table.setColumnCount(self.dataset_table.columnCount() + 1)
        self.dataset_table.setHorizontalHeaderItem(self.dataset_table.columnCount() - 1, QTableWidgetItem('TAG'))

    def set_row(self):
        if self.shared_data.parameter_export_list is not None:
            amount = len(self.shared_data.parameter['TIMECODE'])
            if amount > 100:
                amount = 100

            parameter_list = ['TIMECODE']
            parameter_list.extend(self.shared_data.parameter_export_list)
            parameter_list.append('TAG')

            for i in range(amount):
                self.dataset_table.setRowCount(self.dataset_table.rowCount() + 1)
                for y in range(len(parameter_list)):
                    value = self.shared_data.parameter[parameter_list[y]][i]
                    if type(value) is datetime:
                        value = value.strftime('%H:%M:%S:') + str(int(value.microsecond / 1000))

                    self.dataset_table.setItem(i, y, QTableWidgetItem(value))

    def update_table(self):
        self.dataset_table.clear()
        self.set_columns()
        self.set_row()