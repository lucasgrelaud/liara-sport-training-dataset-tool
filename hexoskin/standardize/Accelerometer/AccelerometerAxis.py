from scipy.io import wavfile
from hexoskin.standardize.Accelerometer.exception.WavImportException import WavImportException


class AccelerometerAxis:
    """Class which represent an axis of the accelerometer"""

    def __init__(self, axis, file_path):
        try:
            self.rate, self.data = wavfile.read(file_path)
        except FileNotFoundError:
            raise WavImportException("The file can\' be found")
        except ValueError:
            raise WavImportException('')
        self.axis = axis
        self.time = self.data.size / self.rate

    def print_result(self):
        print('Sample rate: ', self.rate)
        print('Records: ', self.data.size)
        print('Duration: ', self.time)
        print(self.data)
        return
