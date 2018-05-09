from datetime import datetime
from datetime import timedelta
from scipy.io import wavfile
from .exception.WavImportException import WavImportException


class AccelerometerAxis:
    """Class which represent an axis of the accelerometer"""

    def __init__(self, axis, file_path):
        # Try to import the data from a specific WAV file
        try:
            self.rate, self.raw_data = wavfile.read(file_path)
        except FileNotFoundError:
            raise WavImportException('\nERROR : The file "' + file_path + '" can\'t be found.')
        except ValueError:
            raise WavImportException('The file "' + file_path + '" has been corrupted and cannot be read')

        self.axis = axis
        self.nrecords = self.raw_data.size
        self.time = self.raw_data.size / self.rate
        self.data = {}
        self.add_timecode()

    def get_data(self):
        return self.data

    def print_result(self):
        """
            Print the metadata of the axis record.
        """
        print('Axis: ', self.axis)
        print('Sample rate: ', self.rate)
        print('Records: ', self.raw_data.size)
        print('Duration (seconds): ', self.time)

    def add_timecode(self):
        """
            Generate the records timecode based on the sample rate and
            the recording duration
        """
        timecode = datetime(1970, 1, 1, 0, 0, 0, 0)
        delta = timedelta(microseconds=(1 / self.rate) * 1000000)

        for record in self.raw_data:
            self.data[timecode.strftime('%H:%M:%S:%f')] = record
            timecode = timecode + delta
