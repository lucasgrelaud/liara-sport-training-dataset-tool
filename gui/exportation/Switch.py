# Inspired by https://github.com/bharadwaj-raju/QToggleSwitch/blob/master/QToggleSwitch.py
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QSlider
from PyQt5.QtCore import Qt


class QToggleSwitch(QSlider):

    # Custom signals work only when in decorator
    toggled = pyqtSignal(str, bool)

    def __init__(self, data_label, default=0):

        QSlider.__init__(self, Qt.Horizontal)
        self.setMaximumWidth(30)
        self.setMinimum(0)
        self.setMaximum(1)
        self.setSliderPosition(default)
        self.sliderReleased.connect(self.toggle)
        self.data_label = data_label

    def toggle(self):

        if self.value == 1:
            self.setSliderPosition(0)
            self.setValue(0)
            self.toggled.emit(self.data_label, False)

        else:
            self.setSliderPosition(1)
            self.setValue(0)
            self.toggled.emit(self.data_label, True)

    def isOn(self):
        if self.currentValue == 1:
            return True
        else:
            return False
