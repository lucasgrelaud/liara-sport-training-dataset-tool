from datetime import datetime

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QAbstractItemView
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QTableWidget
from PyQt5.QtWidgets import QTableWidgetItem
from PyQt5.QtWidgets import QVBoxLayout
from PyQt5.QtWidgets import QWidget


class SideBarWidget(QWidget):
    def __init__(self, parent, shared_data):
        super(SideBarWidget, self).__init__(parent)
        self.__shared_data = shared_data
        self.__shared_data.update_sync.connect(self.__update_sync_value)
        self.__shared_data.tags_updated.connect(self.__tags_updated)

        # Create the Sync visualiser
        self.__video_sync_label = QLabel()
        self.__video_sync_label.setText("Video Sync Timecode")

        self.__video_sync_value = QLineEdit()
        self.__video_sync_value.setReadOnly(True)
        self.__video_sync_value.setText('HH:SS:MM:zzz')
        self.__video_sync_value.setMaximumWidth(300)

        self.__data_sync_label = QLabel()
        self.__data_sync_label.setText("Data Sync Timecode")

        self.__data_sync_value = QLineEdit()
        self.__data_sync_value.setReadOnly(True)
        self.__data_sync_value.setText('HH:SS:MM:zzz')
        self.__data_sync_value.setMaximumWidth(300)

        # Create the tags table & controls
        self.__tags_label = QLabel()
        self.__tags_label.setText('Tags list')

        self.__tags_table = QTableWidget()
        self.__tags_table.setRowCount(1)
        self.__tags_table.setColumnCount(2)
        self.__tags_table.setHorizontalHeaderItem(0, QTableWidgetItem('TimeCode'))
        self.__tags_table.setHorizontalHeaderItem(1, QTableWidgetItem('Tag'))
        self.__tags_table.verticalHeader().setVisible(True)
        self.__tags_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.__tags_table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.__tags_table.setSelectionMode(QAbstractItemView.SingleSelection)
        self.__tags_table.setShowGrid(True)
        self.__tags_table.setMinimumHeight(500)
        self.__tags_table.setMaximumHeight(600)

        self.__tags_delete_button = QPushButton()
        self.__tags_delete_button.setText('Delete tag')
        self.__tags_delete_button.setToolTip('Delete tag selected in the table.')
        self.__tags_delete_button.setEnabled(False)
        self.__tags_delete_button.clicked.connect(self.__delete_tag)

        self.__widget_layout = QVBoxLayout()
        self.__widget_layout.setSpacing(10)
        self.__widget_layout.addWidget(self.__video_sync_label)
        self.__widget_layout.addWidget(self.__video_sync_value)
        self.__widget_layout.addWidget(self.__data_sync_label)
        self.__widget_layout.addWidget(self.__data_sync_value)
        self.__widget_layout.addWidget(self.__tags_label)
        self.__widget_layout.addWidget(self.__tags_table)
        self.__widget_layout.addWidget(self.__tags_delete_button)
        self.__widget_layout.addStretch(1)

        self.setLayout(self.__widget_layout)

        self.__restore_state()

    def __update_sync_value(self):
        self.__video_sync_value.setText(self.__shared_data.video_sync)
        self.__data_sync_value.setText(self.__shared_data.data_sync)

    def __delete_tag(self):
        temp_value = self.__tags_table.selectedItems()[0].text().split(':')
        timecode = datetime(1970, 1, 1, int(temp_value[0]), int(temp_value[1]), int(temp_value[2]),
                         int(temp_value[3]) * 1000)
        self.__shared_data.update_tags.emit('delete', timecode, self.__tags_table.selectedItems()[1].text())

    def __tags_updated(self, action, timecode, tag):
        self.__tags_delete_button.setEnabled(True)
        if action == 'add':
            self.__tags_table.setItem(self.__tags_table.rowCount() - 1, 0, QTableWidgetItem(timecode))
            self.__tags_table.setItem(self.__tags_table.rowCount() - 1, 1, QTableWidgetItem(tag))
            self.__tags_table.insertRow(self.__tags_table.rowCount())
        elif action == 'update':
            item = self.__tags_table.findItems(timecode, Qt.MatchExactly)[0]
            self.__tags_table.setCurrentCell(item.row(), item.column())
            self.__tags_table.selectedItems()[1].setText(tag)
        elif action == 'delete':
            item = self.__tags_table.findItems(timecode, Qt.MatchExactly)[0]
            self.__tags_table.removeRow(item.row())

    def __restore_state(self):
        if self.__shared_data.video_sync is not None or self.__shared_data.data_sync is not None:
            self.__update_sync_value()

        # TODO: fix this method
        if self.__shared_data.parameter is not None:
            for i in range(len(self.__shared_data.parameter['TAG'])):
                tag = self.__shared_data.parameter['TAG'][i]
                if tag != '':
                    self.__tags_table.setItem(self.tags_table.rowCount() - 1, 0, QTableWidgetItem(self.__shared_data.parameter['TIMECODE'][i]))
                    self.__tags_table.setItem(self.tags_table.rowCount() - 1, 1, QTableWidgetItem(tag))
                    self.__tags_table.insertRow(self.tags_table.rowCount())