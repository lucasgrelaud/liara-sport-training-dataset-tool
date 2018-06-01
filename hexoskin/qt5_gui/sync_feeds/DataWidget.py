from PyQt5.QtCore import QDir
from PyQt5.QtCore import QTime

from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtWidgets import QTimeEdit
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QStyle
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtWidgets import QHBoxLayout
from PyQt5.QtWidgets import QVBoxLayout

from pyqtgraph import AxisItem
from pyqtgraph import ViewBox
from pyqtgraph import GraphicsView
from pyqtgraph import GraphicsLayout
from pyqtgraph import PlotItem
from pyqtgraph import PlotCurveItem


class DataWidget(QWidget):
    def __init__(self, parent, shared_data):
        super(DataWidget, self).__init__(parent)
        self.shared_data = shared_data
        self.shared_data.data_sync = 'HH:SS:MM:zzz'
        self.shared_data.update.emit()

        # Add the file selection controls
        self.dir_picker_button = QPushButton()
        self.dir_picker_button.setEnabled(True)
        self.dir_picker_button.setIcon(self.style().standardIcon(QStyle.SP_DirIcon))
        self.dir_picker_button.setToolTip('Select the directory using the file explorer')
        self.dir_picker_button.clicked.connect(self.open_dir_picker)

        self.dir_path_input = QLineEdit()
        self.dir_path_input.setPlaceholderText('Path to hexoskin data directory.')
        self.dir_path_input.textEdited.connect(self.manual_file_definition)

        self.load_dir_button = QPushButton('Load data')
        self.load_dir_button.setEnabled(False)
        self.load_dir_button.clicked.connect(self.load_file)

        # Add the sync controls
        self.sync_time_label = QLabel()
        self.sync_time_label.setText('Enter the timecode (HH:mm:ss:zzz) : ')

        self.sync_time_edit = QTimeEdit()
        self.sync_time_edit.setDisplayFormat('HH:mm:ss:zzz')
        self.sync_time_edit.setEnabled(False)

        self.sync_time_button = QPushButton()
        self.sync_time_button.setText('Set sync time')
        self.sync_time_button.setEnabled(False)
        self.sync_time_button.clicked.connect(self.sync_date)

        # Create the layout for the file controls
        dir_layout = QHBoxLayout()
        dir_layout.setContentsMargins(0, 0, 0, 0)
        dir_layout.addWidget(self.dir_picker_button)
        dir_layout.addWidget(self.dir_path_input)
        dir_layout.addWidget(self.load_dir_button)

        # Create the layout for the sync controls
        sync_layout = QHBoxLayout()
        sync_layout.setContentsMargins(0, 0, 0, 0)
        sync_layout.addWidget(self.sync_time_label)
        sync_layout.addWidget(self.sync_time_edit)
        sync_layout.addWidget(self.sync_time_button)
        sync_layout.addStretch(1)

        # Create the axis and their viewbox
        self.x_axis_item = AxisItem('left')
        self.y_axis_item = AxisItem('left')
        self.z_axis_item = AxisItem('left')

        self.x_axis_viewbox = ViewBox()
        self.y_axis_viewbox = ViewBox()
        self.z_axis_viewbox = ViewBox()

        # Create the widget which will display the data
        self.graphic_view = GraphicsView(background="#ecf0f1")
        self.graphic_layout = GraphicsLayout()
        self.graphic_view.setCentralWidget(self.graphic_layout)

        # Add the axis to the widget
        self.graphic_layout.addItem(self.x_axis_item, row=2, col=3, rowspan=1, colspan=1)
        self.graphic_layout.addItem(self.y_axis_item, row=2, col=2, rowspan=1, colspan=1)
        self.graphic_layout.addItem(self.z_axis_item, row=2, col=1, rowspan=1, colspan=1)

        self.plot_item = PlotItem()
        self.plot_item_viewbox = self.plot_item.vb
        self.graphic_layout.addItem(self.plot_item, row=2, col=4, rowspan=1, colspan=1)

        self.graphic_layout.scene().addItem(self.x_axis_viewbox)
        self.graphic_layout.scene().addItem(self.y_axis_viewbox)
        self.graphic_layout.scene().addItem(self.z_axis_viewbox)

        self.x_axis_item.linkToView(self.x_axis_viewbox)
        self.y_axis_item.linkToView(self.y_axis_viewbox)
        self.z_axis_item.linkToView(self.z_axis_viewbox)

        self.x_axis_viewbox.setXLink(self.plot_item_viewbox)
        self.y_axis_viewbox.setXLink(self.plot_item_viewbox)
        self.z_axis_viewbox.setXLink(self.plot_item_viewbox)

        self.x_axis_item.setLabel('Xaxis', color="#34495e")
        self.y_axis_item.setLabel('Yaxis', color="#9b59b6")
        self.z_axis_item.setLabel('Zaxis', color="#3498db")

        self.plot_item_viewbox.sigResized.connect(self.update_views)
        self.x_axis_viewbox.enableAutoRange(axis=ViewBox.XAxis,enable=True)
        self.y_axis_viewbox.enableAutoRange(axis=ViewBox.XAxis, enable=True)
        self.z_axis_viewbox.enableAutoRange(axis=ViewBox.XAxis, enable=True)

        # Create the final layout
        self.v_box = QVBoxLayout()
        self.v_box.addLayout(dir_layout)
        self.v_box.addWidget(self.graphic_view)
        self.v_box.addLayout(sync_layout)

        self.setLayout(self.v_box)

    def open_dir_picker(self):
        self.shared_data.data_dir = QFileDialog.getExistingDirectory(self, 'Open the Hexoskin data directory',
                                                                     QDir.homePath())
        if self.shared_data.data_dir != '':
            self.dir_path_input.setText(self.shared_data.data_dir)
            self.load_dir_button.setEnabled(True)

    def manual_file_definition(self):
        if self.dir_path_input.text() != '':
            self.shared_data.data_dir = self.dir_path_input.text()
            self.load_dir_button.setEnabled(True)

    def load_file(self):
        if self.shared_data.data_dir != '':
            self.shared_data.init_data()
            timecodes = list(self.shared_data.moves.accelerometer.x_axis.timecodes())
            x = list(self.shared_data.moves.accelerometer.x_axis.values())
            y = list(self.shared_data.moves.accelerometer.y_axis.values())
            z = list(self.shared_data.moves.accelerometer.z_axis.values())
            self.sync_time_edit.setEnabled(True)
            self.sync_time_button.setEnabled(True)

            middle = [0] * len(timecodes)
            self.plot_item_viewbox.addItem(PlotCurveItem(middle,  pen='#000000'))
            self.x_axis_viewbox.addItem(PlotCurveItem(x, pen='#34495e'))
            self.y_axis_viewbox.addItem(PlotCurveItem(y, pen='#9b59b6'))
            self.z_axis_viewbox.addItem(PlotCurveItem(z, pen='#3498db'))
            self.plot_item.getAxis('bottom').setTicks(self.generate_time_ticks(timecodes,
                                                                               self.shared_data.moves.accelerometer.rate))

        self.update_views()

    def update_views(self):
        self.x_axis_viewbox.setGeometry(self.plot_item_viewbox.sceneBoundingRect())
        self.y_axis_viewbox.setGeometry(self.plot_item_viewbox.sceneBoundingRect())
        self.z_axis_viewbox.setGeometry(self.plot_item_viewbox.sceneBoundingRect())

    def generate_time_ticks(self, timecodes, rate):
        ticks = list()

        steps = [rate*30, rate*15, rate]
        for step in steps:
            temp = list()
            i = step
            while i in range(len(timecodes)):
                temp.append((i, timecodes[i]))
                i += step
            ticks.append(temp)

        return ticks

    def sync_date(self):
        self.shared_data.data_start_sync = self.sync_time_edit.text()
        self.shared_data.update.emit()