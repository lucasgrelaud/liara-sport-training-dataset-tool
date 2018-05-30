import csv
import os
from datetime import datetime
from datetime import timedelta

from scipy.io import wavfile

from hexoskin.standardize.exception.WavImportException import WavImportException


class ECG:
    """
    Object that represent the ECG data of the test subject.

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
        The path of the directory where the output fill will be generated.
    __file1_sampling_rate : int
        The sampling rate of the file.
    __file1_raw_data : list
        The data stored in the file.
    __file2_sampling_rate : int
        The sampling rate of the file.
    __file2_raw_data : list
        The data stored in the file.
    __file3_sampling_rate : int
        The sampling rate of the file.
    __file3_raw_data : list
        The data stored in the file.
    nrecords: int
        The amount of records for the ECG.
    duration: int
        The duration of the records.
    ecg1: dict
        The ECGI data as {timecode, record}.
    ecg2: dict
        The ECGII data as {timecode, record}.
    ecg3: dict
        The ECGIII data as {timecode, record}.

    Notes
    -----
        * ECG :*
                Frequency: 256 Hz
                Resolution LSB: 0.0064 mV
                Dynamic range: 26 mV
                unit: mV * 0.0064
                Unit (binary download): mV * 0.0064

    """

    def __init__(self, input_dir, output_dir):
        self.__input_dir = input_dir
        self.__output_dir = output_dir

        # Try to import the data from a the first ECG file
        try:
            self.__file1_sampling_rate, self.__file1_raw_data = wavfile.read(self.__input_dir + '/ECG_I.wav')
        except FileNotFoundError:
            self.__file1_sampling_rate = None
            self.__file1_raw_data = None
            raise WavImportException('ERROR : The file "{}/ECG_I.wav" can\'t be found.'.format(self.__input_dir))
        except ValueError:
            self.__file1_sampling_rate = None
            self.__file1_raw_data = None
            raise WavImportException('The file "{}/ECG_I.wav" has been corrupted and cannot be read.'
                                     .format(self.__input_dir))

        # Try to import the data from a the second ECG file
        try:
            self.__file2_sampling_rate, self.__file2_raw_data = wavfile.read(self.__input_dir + '/ECG_II.wav')
        except FileNotFoundError:
            self.__file2_sampling_rate = None
            self.__file2_raw_data = None
            raise WavImportException('ERROR : The file "{}/ECG_II.wav" can\'t be found.'
                                     .format(self.__input_dir))
        except ValueError:
            self.__file2_sampling_rate = None
            self.__file2_raw_data = None
            raise WavImportException('The file "{}/ECG_II.wav" has been corrupted and cannot be read.'
                                     .format(self.__input_dir))

        # Try to import the data from a the third ECG file
        try:
            self.__file3_sampling_rate, self.__file3_raw_data = wavfile.read(self.__input_dir + '/ECG_III.wav')
        except FileNotFoundError:
            self.__file3_sampling_rate = None
            self.__file3_raw_data = None
            raise WavImportException('ERROR : The file "{}/ECG_III.wav" can\'t be found.'
                                     .format(self.__input_dir))
        except ValueError:
            self.__file3_sampling_rate = None
            self.__file3_raw_data = None
            raise WavImportException('The file "/ECG_III.wav has been corrupted and cannot be read.'
                                     .format(self.__input_dir))

        # Test if at least one file have been loaded
        if not self.__file1_sampling_rate and not self.__file2_sampling_rate and not self.__file3_sampling_rate:
            raise WavImportException('The ECG Object can\'t be initialized because all the related'
                                     'files are missing or corrupted.')

        if self.__file1_sampling_rate:
            self.nrecords = self.__file1_raw_data.size
            self.duration = self.__file1_raw_data.size / self.__file1_sampling_rate
        elif self.__file2_sampling_rate:
            self.nrecords = self.__file2_raw_data.size
            self.duration = self.__file2_raw_data.size / self.__file2_sampling_rate
        else:
            self.nrecords = self.__file3_raw_data.size
            self.duration = self.__file3_raw_data.size / self.__file3_sampling_rate
        self.ecg1 = {}
        self.ecg2 = {}
        self.ecg3 = {}
        self.__standardize()

    def __standardize(self):
        """
        Standardize the imported data and add the timecode.
        """
        timecode = datetime(1970, 1, 1, 0, 0, 0, 0)
        delta = timedelta(microseconds=(1 / self.__file1_sampling_rate) * 1000000)

        if self.__file1_sampling_rate:
            for record in self.__file1_raw_data:
                self.ecg1[timecode.strftime('%H:%M:%S:%f')] = record
                timecode = timecode + delta
        timecode = datetime(1970, 1, 1, 0, 0, 0, 0)
        if self.__file2_sampling_rate:
            for record in self.__file2_raw_data:
                self.ecg2[timecode.strftime('%H:%M:%S:%f')] = record
                timecode = timecode + delta
        timecode = datetime(1970, 1, 1, 0, 0, 0, 0)
        if self.__file3_sampling_rate:
            for record in self.__file3_raw_data:
                self.ecg3[timecode.strftime('%H:%M:%S:%f')] = record
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
        Export the standardized data of the related objects to a CSV file.
        """
        # Create the directory if needed
        if not os.path.isdir(self.__output_dir):
            os.mkdir(self.__output_dir)
            print('Create the output directory : "' + self.__output_dir + '".')

        # Generate the CSV
        with open(self.__output_dir + '/ecg.csv', 'w', newline='') as csvfile:
            filewriter = csv.writer(csvfile, dialect='excel')
            filewriter.writerow(['TimeCode', 'ECG_I(mV * 0.0064)', 'ECG_II(mV * 0.0064)', 'ECG_III(mV * 0.0064)'])
            if self.ecg1:
                for timecode in self.ecg1.keys():
                    filewriter.writerow(
                        [timecode, self.ecg1.get(timecode), self.ecg2.get(timecode), self.ecg3.get(timecode)])
            elif self.__file2_sampling_rate:
                for timecode in self.ecg2.keys():
                    filewriter.writerow(
                        [timecode, self.ecg1.get(timecode), self.ecg2.get(timecode), self.ecg3.get(timecode)])
            else:
                for timecode in self.ecg3.keys():
                    filewriter.writerow(
                        [timecode, self.ecg1.get(timecode), self.ecg2.get(timecode), self.ecg3.get(timecode)])
