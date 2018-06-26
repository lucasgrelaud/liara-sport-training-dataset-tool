from datetime import datetime

from PyQt5.QtWidgets import QAbstractItemView
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QTableWidget
from PyQt5.QtWidgets import QTableWidgetItem
from PyQt5.QtWidgets import QVBoxLayout
from PyQt5.QtWidgets import QWidget


class DatasetDisplayWidget(QWidget):

    def __init__(self, parent, shared_data):
        super(DatasetDisplayWidget, self).__init__(parent)
        self.__shared_data = shared_data

        # Create the table
        self.__dataset_label = QLabel()
        self.__dataset_label.setText('Dataset preview :')
        dataset_font = self.__dataset_label.font()
        dataset_font.setBold(True)
        self.__dataset_label.setFont(dataset_font)

        self.__dataset_table = QTableWidget()
        self.__dataset_table.setRowCount(1)
        self.__dataset_table.verticalHeader().setVisible(True)
        self.__dataset_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.__dataset_table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.__dataset_table.setSelectionMode(QAbstractItemView.SingleSelection)
        self.__dataset_table.setShowGrid(True)
        self.__dataset_table.setMinimumHeight(600)

        self.__set_columns()
        self.__set_row()

        main_layout = QVBoxLayout()
        main_layout.addWidget(self.__dataset_label)
        main_layout.addWidget(self.__dataset_table)
        main_layout.addStretch(1)

        self.setLayout(main_layout)

        self.__shared_data.export_list_updated.connect(self.update_table)

    def __set_columns(self):
        self.__dataset_table.setColumnCount(1)
        self.__dataset_table.setHorizontalHeaderItem(0, QTableWidgetItem('TimeCode'))
        if self.__shared_data.parameter_export_list is not None:
            for column_name in self.__shared_data.parameter_export_list:
                self.__dataset_table.setColumnCount(self.__dataset_table.columnCount() + 1)
                self.__dataset_table.setHorizontalHeaderItem(self.__dataset_table.columnCount() - 1,
                                                             QTableWidgetItem(column_name))
        self.__dataset_table.setColumnCount(self.__dataset_table.columnCount() + 1)
        self.__dataset_table.setHorizontalHeaderItem(self.__dataset_table.columnCount() - 1, QTableWidgetItem('TAG'))

    def __set_row(self):
        if self.__shared_data.parameter_export_list is not None:
            amount = len(self.__shared_data.parameter['TIMECODE'])
            if amount > 100:
                amount = 100

            parameter_list = ['TIMECODE']
            parameter_list.extend(self.__shared_data.parameter_export_list)
            parameter_list.append('TAG')

            for i in range(amount):
                self.__dataset_table.setRowCount(self.__dataset_table.rowCount() + 1)
                for y in range(len(parameter_list)):
                    value = self.__shared_data.parameter[parameter_list[y]][i]
                    if type(value) is datetime:
                        value = value.strftime('%H:%M:%S:') + str(int(value.microsecond / 1000))

                    self.__dataset_table.setItem(i, y, QTableWidgetItem(value))

    def update_table(self):
        self.__dataset_table.clear()
        self.__set_columns()
        self.__set_row()
