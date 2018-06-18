from PyQt5.QtCore import Qt

from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QVBoxLayout
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtWidgets import QTableWidget
from PyQt5.QtWidgets import QTableWidgetItem
from PyQt5.QtWidgets import QAbstractItemView
from PyQt5.QtWidgets import QPushButton


class SideBarWidget(QWidget):
    def __init__(self, parent, shared_data):
        super(SideBarWidget, self).__init__(parent)
        self.shared_data = shared_data
        self.shared_data.update_sync.connect(self.update_sync_value)
        self.shared_data.tags_updated.connect(self.tags_updated)

        # Create the Sync visualiser
        self.video_sync_label = QLabel()
        self.video_sync_label.setText("Video Sync Timecode")

        self.video_sync_value = QLineEdit()
        self.video_sync_value.setReadOnly(True)
        self.video_sync_value.setText('HH:SS:MM:zzz')
        self.video_sync_value.setMaximumWidth(300)

        self.data_sync_label = QLabel()
        self.data_sync_label.setText("Data Sync Timecode")

        self.data_sync_value = QLineEdit()
        self.data_sync_value.setReadOnly(True)
        self.data_sync_value.setText('HH:SS:MM:zzz')
        self.data_sync_value.setMaximumWidth(300)

        # Create the tags table & controls
        self.tags_label = QLabel()
        self.tags_label.setText('Tags list')

        self.tags_table = QTableWidget()
        self.tags_table.setRowCount(1)
        self.tags_table.setColumnCount(2)
        self.tags_table.setHorizontalHeaderItem(0, QTableWidgetItem('TimeCode'))
        self.tags_table.setHorizontalHeaderItem(1, QTableWidgetItem('Tag'))
        self.tags_table.verticalHeader().setVisible(False)
        self.tags_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tags_table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.tags_table.setSelectionMode(QAbstractItemView.SingleSelection)
        self.tags_table.setShowGrid(True)
        self.tags_table.setMinimumHeight(500)
        self.tags_table.setMaximumHeight(600)

        self.tags_delete_button = QPushButton()
        self.tags_delete_button.setText('Delete tag')
        self.tags_delete_button.setToolTip('Delete tag selected in the table.')
        self.tags_delete_button.setEnabled(False)
        self.tags_delete_button.clicked.connect(self.delete_tag)

        self.widget_layout = QVBoxLayout()
        self.widget_layout.setSpacing(10)
        self.widget_layout.addWidget(self.video_sync_label)
        self.widget_layout.addWidget(self.video_sync_value)
        self.widget_layout.addWidget(self.data_sync_label)
        self.widget_layout.addWidget(self.data_sync_value)
        self.widget_layout.addWidget(self.tags_label)
        self.widget_layout.addWidget(self.tags_table)
        self.widget_layout.addWidget(self.tags_delete_button)
        self.widget_layout.addStretch(1)

        self.setLayout(self.widget_layout)

        self.restore_state()

    def update_sync_value(self):
        self.video_sync_value.setText(self.shared_data.video_sync)
        self.data_sync_value.setText(self.shared_data.data_sync)

    def delete_tag(self):
        self.shared_data.update_tags.emit('delete', self.tags_table.selectedItems()[0].text(),
                                          self.tags_table.selectedItems()[1].text(),)

    def tags_updated(self, action, timecode, tag):
        if action == 'add':
            self.tags_table.setItem(self.tags_table.rowCount()-1, 0, QTableWidgetItem(timecode))
            self.tags_table.setItem(self.tags_table.rowCount()-1, 1, QTableWidgetItem(tag))
            self.tags_table.insertRow(self.tags_table.rowCount())
        elif action == 'delete':
            item = self.tags_table.findItems(timecode, Qt.MatchExactly)[0]
            self.tags_table.removeRow(item.row())
        elif action == 'update':
            item = self.tags_table.findItems(timecode, Qt.MatchExactly)[0]
            self.tags_table.setCurrentCell(item.row(), item.column())
            self.tags_table.selectedItems()[1].setText(tag)

        if len(self.shared_data.tags) == 0:
            self.tags_delete_button.setEnabled(False)
        else:
            self.tags_delete_button.setEnabled(True)

    def restore_state(self):
        if self.shared_data.video_sync != 'HH:SS:MM:zzz' or self.shared_data.data_sync != 'HH:SS:MM:zzz':
            self.update_sync_value()

        if len(self.shared_data.tags) != 0:
            for key, value in self.shared_data.tags.items():
                self.tags_table.setItem(self.tags_table.rowCount() - 1, 0, QTableWidgetItem(key))
                self.tags_table.setItem(self.tags_table.rowCount() - 1, 1, QTableWidgetItem(value))
                self.tags_table.insertRow(self.tags_table.rowCount())