from datetime import datetime
from datetime import timedelta
from scipy.io import wavfile
from hexoskin.standardize.Accelerometer.exception.WavImportException import WavImportException


class AccelerometerAxis:
    """Class which represent an axis of the accelerometer"""

    def __init__(self, axis, file_path):
        try:
            self.rate, self.raw_data = wavfile.read(file_path)
        except FileNotFoundError:
            raise WavImportException('\nERROR : The file "' + file_path + '" can\'t be found.')
        except ValueError:
            raise WavImportException('')

        self.axis = axis
        self.nrecords = self.raw_data.size
        self.time = self.raw_data.size / self.rate
        self.data = {}
        self.add_timecode()

    def print_result(self):
        print('Axis: ', self.axis)
        print('Sample rate: ', self.rate)
        print('Records: ', self.raw_data.size)
        print('Duration (seconds): ', self.time)
        return

    def add_timecode(self):
        timecode = datetime(1970, 1, 1, 0, 0, 0, 0)

        for record in self.raw_data:
            self.data[timecode.strftime('%H:%M:%S:%f')] = record
            timecode = timecode + timedelta(microseconds=15625)
