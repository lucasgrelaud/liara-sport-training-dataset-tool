from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QVBoxLayout
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtWidgets import QTableWidget
from PyQt5.QtWidgets import QTableWidgetItem
from PyQt5.QtWidgets import QAbstractItemView


class SideBarWidget(QWidget):
    def __init__(self, parent, shared_data):
        super(SideBarWidget, self).__init__(parent)
        self.shared_data = shared_data
        self.shared_data.update_sync.connect(self.update_sync_value)
        self.shared_data.update_tags.connect(self.update_tags)

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

        self.tags_label = QLabel()
        self.tags_label.setText('Tags list')

        self.tags_table = QTableWidget()
        self.tags_table.setHorizontalHeaderItem(1, QTableWidgetItem('TimeCode'))
        self.tags_table.setHorizontalHeaderItem(2, QTableWidgetItem('Tag'))
        self.tags_table.verticalHeader().setVisible(False)
        self.tags_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tags_table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.tags_table.setSelectionMode(QAbstractItemView.MultiSelection)
        self.tags_table.setShowGrid(False)

        self.v_layout = QVBoxLayout()
        self.v_layout.setSpacing(10)
        self.v_layout.addWidget(self.video_sync_label)
        self.v_layout.addWidget(self.video_sync_value)
        self.v_layout.addWidget(self.data_sync_label)
        self.v_layout.addWidget(self.data_sync_value)
        self.v_layout.addWidget(self.tags_label)
        self.v_layout.addWidget(self.tags_table)
        self.v_layout.addStretch(1)

        self.setLayout(self.v_layout)

    def update_sync_value(self):
        self.video_sync_value.setText(self.shared_data.video_sync)
        self.data_sync_value.setText(self.shared_data.data_sync)

    def update_tags(self, state):
        if state == 'add':
            print(sorted(self.shared_data.tags))