from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QVBoxLayout
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QLineEdit


class SideBarWidget(QWidget):
    def __init__(self, parent, shared_data):
        super(SideBarWidget, self).__init__(parent)
        self.shared_data = shared_data
        # self.shared_data.update.connect(self.update_sync_value)
        self.shared_data.update.connect(self.update_sync_value)

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

        self.v_layout = QVBoxLayout()
        self.v_layout.setSpacing(10)
        self.v_layout.addWidget(self.video_sync_label)
        self.v_layout.addWidget(self.video_sync_value)
        self.v_layout.addWidget(self.data_sync_label)
        self.v_layout.addWidget(self.data_sync_value)
        self.v_layout.addStretch(1)

        self.setLayout(self.v_layout)

    def update_sync_value(self):
        self.video_sync_value.setText(self.shared_data.video_sync)
        self.data_sync_value.setText(self.shared_data.data_sync)