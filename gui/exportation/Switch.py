from PyQt5.QtCore import Qt
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QSlider


class QToggleSwitch(QSlider):
    toggled = pyqtSignal()
    switchedOn = pyqtSignal(str)
    switchedOff = pyqtSignal(str)

    def __init__(self, label, default=0):

        QSlider.__init__(self, Qt.Horizontal)
        self.setMaximumWidth(30)
        self.setMinimum(0)
        self.setMaximum(1)
        self.setSliderPosition(default)

        self.sliderReleased.connect(self.toggle)
        self.__label = label
        self.__last_value = self.value()

    def toggle(self):
        if self.value() == 0:

            if self.__last_value != 0:
                self.toggled.emit()
                self.switchedOff.emit(self.__label)
                self.__last_value = 0

        else:
            if self.__last_value != 1:
                self.toggled.emit()
                self.switchedOn.emit(self.__label)
                self.__last_value = 1

    def isOn(self):
        if self.currentValue == 1:
            return True
        else:
            return False
