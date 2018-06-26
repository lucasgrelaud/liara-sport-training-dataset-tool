from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QVBoxLayout
from PyQt5.QtWidgets import QHBoxLayout
from PyQt5.QtGui import QFont

from .Switch import QToggleSwitch


class ExportSelectorWidget(QWidget):

    def __init__(self, parent, shared_data):
        super(ExportSelectorWidget, self).__init__(parent)
        self.__shared_data = shared_data

        # Create the header
        self.__select_label = QLabel()
        self.__select_label.setText('Select the desired parameters :')
        select_font = self.__select_label.font()
        select_font.setBold(True)
        self.__select_label.setFont(select_font)

        # Generate the selectors column
        self.__column_array = []
        if self.__shared_data.parameter is not None:
            selectable_parameter_list = sorted(self.__shared_data.parameter.keys() - {'TIMECODE', 'TAG'})
            for i in range(len(selectable_parameter_list)):
                if i % 5 == 0:
                    self.__column_array.append(QVBoxLayout())
                line = QHBoxLayout()
                label = QLabel(selectable_parameter_list[i])
                switch = QToggleSwitch(selectable_parameter_list[i], default=1)
                switch.switchedOn.connect(self.__switch_toggledOn)
                switch.switchedOff.connect(self.__switch_toggledOff)
                line.addWidget(switch)
                line.addWidget(label)
                line.addStretch(1)
                self.__column_array[len(self.__column_array) - 1].addLayout(line)

        # Generate the selector row
        self.__row_array = []
        if len(self.__column_array) != 0:
            for i in range(len(self.__column_array)):
                if i % 3 == 0:
                    self.__row_array.append(QHBoxLayout())
                self.__row_array[len(self.__row_array) - 1].addLayout(self.__column_array[i])

        # Create the final layout
        main_layout = QVBoxLayout()
        main_layout.addWidget(self.__select_label)
        main_layout.addSpacing(10)
        # Add each selector row the layout
        if len(self.__row_array) != 0:
            for row in self.__row_array:
                main_layout.addLayout(row)
        else:
            main_layout.addWidget(QLabel("There is no parameter to select, have you imported any data ?"))

        self.setLayout(main_layout)

    def __switch_toggledOn(self, parameter):
        self.__shared_data.update_export_list.emit(parameter, True)

    def __switch_toggledOff(self, parameter):
        self.__shared_data.update_export_list.emit(parameter, False)
