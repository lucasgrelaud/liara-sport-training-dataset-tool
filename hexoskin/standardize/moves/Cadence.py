import csv
import os
from datetime import datetime
from datetime import timedelta

from scipy.io import wavfile

from hexoskin.standardize.exception import WavImportException


class Cadence:
    """
    Object that represent the Cadence data of the test subject.

    Parameters
    ----------
    input_dir : str
        The path of the input data that will be imported.
    output_dir : str
        The path of the output data that will be generated.

    Attributes
    ----------
    __input_dir: str
        The path of the directory where are located the files to import.
    __output_dir: str
    __file1_sampling_rate : int
        The sampling rate of the file.
    __file1_raw_data : list
        The data stored in the file.
    nrecords: int
        The amount of records for the cadence.
    duration: int
        The duration of the records.
        The path of the directory where the output fill will be generated.
    cadence : AccelerometerAxis
        The data stored in the file.

    Notes
    -----
        * Cadence *
                Method of calculation:
                    Highpass at 2.65 Hz on the 3 axis independently
                    Vector of acceleration. (accX^2 + accY^2+accZ^2)^.5
                    Averaged over the last second
                Frequency: 1 Hz
                Resolution 3.9 mG.
                Dynamic range +- 16G
                unit G
                Unit (binary download): G/256
    """

    def __init__(self, input_dir, output_dir):
        self.__input_dir = input_dir
        self.__output_dir = output_dir

        # Try to import the data from a specific WAV file
        try:
            self.__file1_sampling_rate, self.__file1_raw_data = wavfile.read(self.__input_dir + '/cadence.wav')
        except FileNotFoundError:
            raise WavImportException('ERROR : The file "{}/cadence.wav" can\'t be found.'
                                     .format(self.__input_dir))
        except ValueError:
            raise WavImportException('The file "{}/cadence.wav" has been corrupted and cannot be read.'
                                     .format(self.__input_dir))

        self.nrecords = self.__file1_raw_data.size
        self.duration = self.__file1_raw_data.size / self.__file1_sampling_rate
        self.cadence = {}
        self.__standardize()

    def __standardize(self):
        """
         Standardize the imported data and add the timecode.
        """
        timecode = datetime(1970, 1, 1, 0, 0, 0, 0)
        delta = timedelta(microseconds=(1 / self.__file1_sampling_rate) * 1000000)

        for record in self.__file1_raw_data:
            key = timecode.strftime('%H:%M:%S:') + str(int(timecode.microsecond / 1000))
            self.cadence[key] = record
            timecode = timecode + delta

    def set_output_dir(self, dir_path):
        """
        Set the output_dir after the initialisation of the object

        Parameters
        ----------
        dir_path : str
            The path of the directory where the output fill will be generated.
        """
        self.__output_dir = dir_path

    def export_csv(self):
        """
        Export the cadence to a CSV file.
        """
        # Create the directory if needed
        if not os.path.isdir(self.__output_dir):
            os.mkdir(self.__output_dir)
            print('Create the output directory : "' + self.__output_dir + '".')

        # Generate the CSV
        with open(self.__output_dir + '/cadence.csv', 'w', newline='') as csvfile:
            filewriter = csv.writer(csvfile, dialect='excel')
            filewriter.writerow(['TimeCode', 'Cadence(Step/min)'])
            for timecode in self.cadence.keys():
                filewriter.writerow([timecode, self.cadence.get(timecode)])
