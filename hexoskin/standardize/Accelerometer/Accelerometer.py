from hexoskin.standardize.Accelerometer.AccelerometerAxis import AccelerometerAxis
from hexoskin.standardize.Accelerometer.exception.WavImportException import WavImportException

class Accelerometer :
    """"Class which represent the accelerometer"""

    def __init__(self, dir_path):
        self.dir_path = dir_path
        try:
            self.x_axis = AccelerometerAxis('x', dir_path + "/acceleration_X.wav")
            self.x_axis = AccelerometerAxis('y', dir_path + "/acceleration_Y.wav")
            self.x_axis = AccelerometerAxis('z', dir_path + "/acceleration_Z.wav")
        except WavImportException:
            exit(1)