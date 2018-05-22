from datetime import datetime
from datetime import timedelta

from scipy.io import wavfile

from hexoskin.standardize.exception.WavImportException import WavImportException


class AccelerometerAxis:
    """
    Object that represent the Accelerometer axis data of the test subject.

    Parameters
    ----------
    axis : str
        The label of the axis.
    file_path : str
        The path the file to import.

    Attributes
    ----------
    axis : AccelerometerAxis
        The data stored in the file.
    nrecords: int
        The amount of records for the accelerometer axis.
    duration: int
        The duration of the records.


    """

    def __init__(self, axis, file_path):
        # Try to import the data from a specific WAV file
        try:
            self._rate, self.__raw_data = wavfile.read(file_path)
        except FileNotFoundError:
            raise WavImportException('ERROR : The file "{}" can\'t be found.'.format(file_path))
        except ValueError:
            raise WavImportException('ERROR : The file "{}" has been corrupted and cannot be read'
                                     .format(file_path))

        self.__axis_raw_data = axis
        self.nrecords = self.__raw_data.size
        self.duration = self.__raw_data.size / self._rate
        self.axis = {}
        self.__standardize()

    def __standardize(self):
        """
        Standardize the imported data and add the timecode.
        """
        timecode = datetime(1970, 1, 1, 0, 0, 0, 0)
        delta = timedelta(microseconds=(1 / self._rate) * 1000000)

        for record in self.__raw_data:
            self.axis[timecode.strftime('%H:%M:%S:%f')] = record
            timecode = timecode + delta
