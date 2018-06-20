from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QVBoxLayout
from PyQt5.QtWidgets import QHBoxLayout
from PyQt5.QtGui import QFont

from .Switch import QToggleSwitch


class ExportSelectorWidget(QWidget):

    def __init__(self, parent, shared_data):
        super(ExportSelectorWidget, self).__init__(parent)
        self.shared_data = shared_data

        # Create the header
        self.select_label = QLabel()
        self.select_label.setText('Select the desired parameters :')
        select_font = self.select_label.font()
        select_font.setBold(True)
        self.select_label.setFont(select_font)


        # Create the breathing selector
        self.breathing_label = QLabel()
        self.breathing_label.setText('Breathing')

        breathing_line_1_h_box = QHBoxLayout()
        self.breathing_line_1_switch = QToggleSwitch('breathing_rate')
        self.breathing_line_1_label = QLabel()
        self.breathing_line_1_label.setText('Breathing Rate')
        breathing_line_1_h_box.addWidget(self.breathing_line_1_switch)
        breathing_line_1_h_box.addWidget(self.breathing_line_1_label)

        breathing_line_2_h_box = QHBoxLayout()
        self.breathing_line_2_switch = QToggleSwitch('expiration')
        self.breathing_line_2_label = QLabel()
        self.breathing_line_2_label.setText('Expiration')
        breathing_line_2_h_box.addWidget(self.breathing_line_2_switch)
        breathing_line_2_h_box.addWidget(self.breathing_line_2_label)

        breathing_line_3_h_box = QHBoxLayout()
        self.breathing_line_3_switch = QToggleSwitch('inspiration')
        self.breathing_line_3_label = QLabel()
        self.breathing_line_3_label.setText('Inspiration')
        breathing_line_3_h_box.addWidget(self.breathing_line_3_switch)
        breathing_line_3_h_box.addWidget(self.breathing_line_3_label)

        breathing_line_4_h_box = QHBoxLayout()
        self.breathing_line_4_switch = QToggleSwitch('respiration')
        self.breathing_line_4_label = QLabel()
        self.breathing_line_4_label.setText('Respiration')
        breathing_line_4_h_box.addWidget(self.breathing_line_4_switch)
        breathing_line_4_h_box.addWidget(self.breathing_line_4_label)

        breathing_line_5_h_box = QHBoxLayout()
        self.breathing_line_5_switch = QToggleSwitch('minute_ventilation')
        self.breathing_line_5_label = QLabel()
        self.breathing_line_5_label.setText('Minute Ventilation')
        breathing_line_5_h_box.addWidget(self.breathing_line_5_switch)
        breathing_line_5_h_box.addWidget(self.breathing_line_5_label)

        breathing_line_6_h_box = QHBoxLayout()
        self.breathing_line_6_switch = QToggleSwitch('tidal_volume')
        self.breathing_line_6_label = QLabel()
        self.breathing_line_6_label.setText('Tidal Volume')
        breathing_line_6_h_box.addWidget(self.breathing_line_6_switch)
        breathing_line_6_h_box.addWidget(self.breathing_line_6_label)

        breathing_v_box = QVBoxLayout()
        breathing_v_box.addWidget(self.breathing_label)
        breathing_v_box.addLayout(breathing_line_1_h_box)
        breathing_v_box.addLayout(breathing_line_2_h_box)
        breathing_v_box.addLayout(breathing_line_3_h_box)
        breathing_v_box.addLayout(breathing_line_4_h_box)
        breathing_v_box.addLayout(breathing_line_5_h_box)
        breathing_v_box.addLayout(breathing_line_6_h_box)
        breathing_v_box.addStretch(1)

        # Create the cardiology selector
        self.cardiology_label = QLabel()
        self.cardiology_label.setText('Cardiology')

        cardiology_line_1_h_box = QHBoxLayout()
        self.cardiology_line_1_switch = QToggleSwitch('ecg')
        self.cardiology_line_1_label = QLabel()
        self.cardiology_line_1_label.setText('ECG')
        cardiology_line_1_h_box.addWidget(self.cardiology_line_1_switch)
        cardiology_line_1_h_box.addWidget(self.cardiology_line_1_label)

        cardiology_line_2_h_box = QHBoxLayout()
        self.cardiology_line_2_switch = QToggleSwitch('heart_rate')
        self.cardiology_line_2_label = QLabel()
        self.cardiology_line_2_label.setText('Heart Rate')
        cardiology_line_2_h_box.addWidget(self.cardiology_line_2_switch)
        cardiology_line_2_h_box.addWidget(self.cardiology_line_2_label)

        cardiology_line_3_h_box = QHBoxLayout()
        self.cardiology_line_3_switch = QToggleSwitch('rr_interval')
        self.cardiology_line_3_label = QLabel()
        self.cardiology_line_3_label.setText('RR Interval')
        cardiology_line_3_h_box.addWidget(self.cardiology_line_3_switch)
        cardiology_line_3_h_box.addWidget(self.cardiology_line_3_label)

        cardiology_v_box = QVBoxLayout()
        cardiology_v_box.addWidget(self.cardiology_label)
        cardiology_v_box.addLayout(cardiology_line_1_h_box)
        cardiology_v_box.addLayout(cardiology_line_2_h_box)
        cardiology_v_box.addLayout(cardiology_line_3_h_box)
        cardiology_v_box.addStretch(1)

        # Create the moves selector
        self.moves_label = QLabel()
        self.moves_label.setText('Moves')

        moves_line_1_h_box = QHBoxLayout()
        self.moves_line_1_switch = QToggleSwitch('accelerometer')
        self.moves_line_1_label = QLabel()
        self.moves_line_1_label.setText('Accelerometer')
        moves_line_1_h_box.addWidget(self.moves_line_1_switch)
        moves_line_1_h_box.addWidget(self.moves_line_1_label)

        moves_line_2_h_box = QHBoxLayout()
        self.moves_line_2_switch = QToggleSwitch('activity')
        self.moves_line_2_label = QLabel()
        self.moves_line_2_label.setText('Activity')
        moves_line_2_h_box.addWidget(self.moves_line_2_switch)
        moves_line_2_h_box.addWidget(self.moves_line_2_label)

        moves_line_3_h_box = QHBoxLayout()
        self.moves_line_3_switch = QToggleSwitch('cadence')
        self.moves_line_3_label = QLabel()
        self.moves_line_3_label.setText('Cadence')
        moves_line_3_h_box.addWidget(self.moves_line_3_switch)
        moves_line_3_h_box.addWidget(self.moves_line_3_label)

        moves_line_4_h_box = QHBoxLayout()
        self.moves_line_4_switch = QToggleSwitch('device_position')
        self.moves_line_4_label = QLabel()
        self.moves_line_4_label.setText('Device Position')
        moves_line_4_h_box.addWidget(self.moves_line_4_switch)
        moves_line_4_h_box.addWidget(self.moves_line_4_label)

        moves_line_5_h_box = QHBoxLayout()
        self.moves_line_5_switch = QToggleSwitch('step')
        self.moves_line_5_label = QLabel()
        self.moves_line_5_label.setText('Step')
        moves_line_5_h_box.addWidget(self.moves_line_5_switch)
        moves_line_5_h_box.addWidget(self.moves_line_5_label)

        moves_v_box = QVBoxLayout()
        moves_v_box.addWidget(self.moves_label)
        moves_v_box.addLayout(moves_line_1_h_box)
        moves_v_box.addLayout(moves_line_2_h_box)
        moves_v_box.addLayout(moves_line_3_h_box)
        moves_v_box.addLayout(moves_line_4_h_box)
        moves_v_box.addLayout(moves_line_5_h_box)
        moves_v_box.addStretch(1)

        # Create the final layout
        h_box_layout = QHBoxLayout()
        h_box_layout.addLayout(breathing_v_box)
        h_box_layout.addLayout(cardiology_v_box)
        h_box_layout.addLayout(moves_v_box)

        main_layout = QVBoxLayout()
        main_layout.addWidget(self.select_label)
        main_layout.addSpacing(10)
        main_layout.addLayout(h_box_layout)

        self.setLayout(main_layout)

