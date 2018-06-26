from PyQt5.QtCore import QDir
from PyQt5.QtCore import QTime
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtWidgets import QHBoxLayout
from PyQt5.QtWidgets import QInputDialog
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QStyle
from PyQt5.QtWidgets import QTimeEdit
from PyQt5.QtWidgets import QVBoxLayout
from PyQt5.QtWidgets import QWidget
from pyqtgraph import AxisItem
from pyqtgraph import GraphicsLayout
from pyqtgraph import GraphicsView
from pyqtgraph import PlotCurveItem
from pyqtgraph import PlotItem
from pyqtgraph import ViewBox


class DataWidget(QWidget):
    def __init__(self, parent, shared_data):
        super(DataWidget, self).__init__(parent)
        self.__shared_data = shared_data
        self.__shared_data.update_sync.emit()

        # Add the file selection controls
        self.__dir_picker_button = QPushButton()
        self.__dir_picker_button.setEnabled(True)
        self.__dir_picker_button.setText("Load data")
        self.__dir_picker_button.setIcon(self.style().standardIcon(QStyle.SP_DirIcon))
        self.__dir_picker_button.setToolTip('Select the directory using the file explorer')
        self.__dir_picker_button.clicked.connect(self.__open_dir_picker)

        # Add the sync controls
        self.__sync_time_label = QLabel()
        self.__sync_time_label.setText('Enter the timecode (HH:mm:ss:zzz) : ')

        self.__sync_time_edit = QTimeEdit()
        self.__sync_time_edit.setDisplayFormat('HH:mm:ss:zzz')
        self.__sync_time_edit.setEnabled(False)

        self.__sync_time_button = QPushButton()
        self.__sync_time_button.setText('Sync data')
        self.__sync_time_button.setEnabled(False)
        self.__sync_time_button.clicked.connect(self.__sync_data)

        # Create the layout for the file controls
        dir_layout = QHBoxLayout()
        dir_layout.setContentsMargins(0, 0, 0, 0)
        dir_layout.addWidget(self.__dir_picker_button)
        dir_layout.addStretch(1)
        dir_layout.addWidget(self.__sync_time_label)
        dir_layout.addWidget(self.__sync_time_edit)
        dir_layout.addWidget(self.__sync_time_button)

        # Create the axis and their viewbox
        self.__x_axis_item = AxisItem('left')
        self.__y_axis_item = AxisItem('left')
        self.__z_axis_item = AxisItem('left')

        self.__x_axis_viewbox = ViewBox()
        self.__y_axis_viewbox = ViewBox()
        self.__z_axis_viewbox = ViewBox()

        # Create the widget which will display the data
        self.__graphic_view = GraphicsView(background="#ecf0f1")
        self.__graphic_layout = GraphicsLayout()
        self.__graphic_view.setCentralWidget(self.__graphic_layout)

        # Add the axis to the widget
        self.__graphic_layout.addItem(self.__x_axis_item, row=2, col=3, rowspan=1, colspan=1)
        self.__graphic_layout.addItem(self.__y_axis_item, row=2, col=2, rowspan=1, colspan=1)
        self.__graphic_layout.addItem(self.__z_axis_item, row=2, col=1, rowspan=1, colspan=1)

        self.__plot_item = PlotItem()
        self.__plot_item_viewbox = self.__plot_item.vb
        self.__graphic_layout.addItem(self.__plot_item, row=2, col=4, rowspan=1, colspan=1)

        self.__graphic_layout.scene().addItem(self.__x_axis_viewbox)
        self.__graphic_layout.scene().addItem(self.__y_axis_viewbox)
        self.__graphic_layout.scene().addItem(self.__z_axis_viewbox)

        self.__x_axis_item.linkToView(self.__x_axis_viewbox)
        self.__y_axis_item.linkToView(self.__y_axis_viewbox)
        self.__z_axis_item.linkToView(self.__z_axis_viewbox)

        self.__x_axis_viewbox.setXLink(self.__plot_item_viewbox)
        self.__y_axis_viewbox.setXLink(self.__plot_item_viewbox)
        self.__z_axis_viewbox.setXLink(self.__plot_item_viewbox)

        self.__x_axis_item.setLabel('ACC_X', color="#34495e")
        self.__y_axis_item.setLabel('ACC_Y', color="#9b59b6")
        self.__z_axis_item.setLabel('ACC_Z', color="#3498db")

        self.__plot_item_viewbox.sigResized.connect(self.__update_views)
        self.__x_axis_viewbox.enableAutoRange(axis=ViewBox.XAxis, enable=True)
        self.__y_axis_viewbox.enableAutoRange(axis=ViewBox.XAxis, enable=True)
        self.__z_axis_viewbox.enableAutoRange(axis=ViewBox.XAxis, enable=True)

        # Create the final layout
        self.__v_box = QVBoxLayout()
        self.__v_box.addLayout(dir_layout)
        self.__v_box.addWidget(self.__graphic_view)

        self.setLayout(self.__v_box)

        self.__restore_state()

    def __open_dir_picker(self):
        self.__shared_data.data_file_path = QFileDialog.getOpenFileUrl(self, 'Open the Hexoskin data directory',
                                                                       QDir.homePath())[0]
        if self.__shared_data.data_file_path is not None:
            try:
                self.__load_files('ACC_X', 'ACC_Y', 'ACC_Z')
            except FileNotFoundError:
                pass
            except UnicodeDecodeError:
                pass

    def __load_files(self, field1, field2, field3):
        if self.__shared_data.data_file_path is not None:
            # Import the parameters from the file
            self.__shared_data.import_parameter()

            # Generate the timecodes if needed
            if len(self.__shared_data.parameter['TIMECODE']) == 0:
                if self.__shared_data.sampling_rate is None:
                    result = False
                    while not result:
                        result = self.__show_sampling_rate_picker()

                self.__shared_data.add_timecode()

            # Show the 3 selected fields
            self.__x_axis_viewbox.addItem(PlotCurveItem(list(map(int, self.__shared_data.parameter.get(field1))),
                                                        pen='#34495e'))
            self.__y_axis_viewbox.addItem(PlotCurveItem(list(map(int, self.__shared_data.parameter.get(field2))),
                                                        pen='#9b59b6'))
            self.__z_axis_viewbox.addItem(PlotCurveItem(list(map(int, self.__shared_data.parameter.get(field3))),
                                                        pen='#3498db'))
            # Add the middle line and the bottom timecodes
            timecodes = self.__shared_data.parameter['TIMECODE']
            middle = [0] * len(timecodes)
            self.__plot_item_viewbox.addItem(PlotCurveItem(middle, pen='#000000'))
            self.__plot_item.getAxis('bottom').setTicks(
                self.__generate_time_ticks(timecodes, self.__shared_data.sampling_rate))

            # Enable the controls
            self.__sync_time_edit.setEnabled(True)
            self.__sync_time_button.setEnabled(True)
            self.__dir_picker_button.setEnabled(False)
        self.__update_views()

    def __update_views(self):
        self.__x_axis_viewbox.setGeometry(self.__plot_item_viewbox.sceneBoundingRect())
        self.__y_axis_viewbox.setGeometry(self.__plot_item_viewbox.sceneBoundingRect())
        self.__z_axis_viewbox.setGeometry(self.__plot_item_viewbox.sceneBoundingRect())

    def __generate_time_ticks(self, timecodes, rate):
        ticks = list()

        steps = [rate * 30, rate * 15, rate]
        for step in steps:
            temp = list()
            i = step
            while i in range(len(timecodes)):
                temp.append((i, timecodes[i].strftime('%H:%M:%S:') + str(int(timecodes[i].microsecond / 1000))))
                i += step
            ticks.append(temp)

        return ticks

    def __sync_data(self):
        self.__shared_data.data_sync = self.__sync_time_edit.text()
        self.__shared_data.update_sync.emit()

    def __show_sampling_rate_picker(self) -> bool:
        self.__shared_data.sampling_rate, result = QInputDialog.getInt(self, 'Set sampling rate value', 'Sampling rate')
        return result

    def __restore_state(self):
        if self.__shared_data.data_file_path is not None:
            self.__load_files('ACC_X', 'ACC_Y', 'ACC_Z')
        if self.__shared_data.data_sync is not None:
            text_time = self.__shared_data.data_sync.split(':')
            time = QTime()
            time.setHMS(int(text_time[0]), int(text_time[1]), int(text_time[2]), int(text_time[3]))
            self.__sync_time_edit.setTime(time)
