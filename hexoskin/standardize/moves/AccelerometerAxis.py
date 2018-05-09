from datetime import datetime
from datetime import timedelta
from scipy.io import wavfile
from .exception.WavImportException import WavImportException


class AccelerometerAxis:
    """Class which represent an axis of the accelerometer"""

    def __init__(self, axis, file_path):
        # Try to import the data from a specific WAV file
        try:
            self._rate, self.__raw_data = wavfile.read(file_path)
        except FileNotFoundError:
            raise WavImportException('\nERROR : The file "' + file_path + '" can\'t be found.')
        except ValueError:
            raise WavImportException('The file "' + file_path + '" has been corrupted and cannot be read')

        self.__axis = axis
        self.__nrecords = self.__raw_data.size
        self.__time = self.__raw_data.size / self._rate
        self.__data = {}
        self.__add_timecode()

    def get_axis(self):
        return self.__axis

    def get_time(self):
        return self.__time

    def get_nrecords(self):
        return self.__nrecords

    def get_data(self):
        return self.__data

    def print_result(self):
        """
            Print the metadata of the axis record.
        """
        print('Axis: ', self.__axis)
        print('Sample rate: ', self._rate)
        print('Records: ', self.__raw_data.size)
        print('Duration (seconds): ', self.__time)

    def __add_timecode(self):
        """
            Generate the records timecode based on the sample rate and
            the recording duration
        """
        timecode = datetime(1970, 1, 1, 0, 0, 0, 0)
        delta = timedelta(microseconds=(1 / self._rate) * 1000000)

        for record in self.__raw_data:
            self.__data[timecode.strftime('%H:%M:%S:%f')] = record
            timecode = timecode + delta
