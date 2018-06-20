import csv
import os
from datetime import datetime
from datetime import timedelta

from scipy.io import wavfile

from hexoskin.standardize.exception.WavImportException import WavImportException


class MinuteVentilation:
    """
    Object that represent the minute ventilation data of the test subject.

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
    nrecords: int
        The amount of records for the minute ventilation.
    duration: int
        The duration of the records.
    minute_ventilation: dict
        The minute_ventilation data as {timecode, record}
    minute_ventilation_quality: dict
        The minute_ventilation_quality data as {timecode, record}

    Notes
    -----
        *Minute ventilation :*
                Frequency: 1 Hz
                Average: last 7 respiration cycles
                Valid range: (2 to 60 RPM)
                    If BR > 60: Clip to 60
                    If BR < 2: set to 2
                Unit: respiration per minute



    """
    def __init__(self, input_dir, output_dir):
        self.__input_dir = input_dir
        self.__output_dir = output_dir

        # Try to import the data from a specific WAV file
        try:
            self.__file1_sampling_rate, self.__file1_raw_data = wavfile.read(self.__input_dir
                                                                             + '/minute_ventilation.wav')
        except FileNotFoundError:
            self.__file1_sampling_rate = None
            self.__file1_raw_data = None
            raise WavImportException('ERROR : The file "{}/minute_ventilation.wav" can\'t be found.'
                                     .format(self.__input_dir))
        except ValueError:
            self.__file1_sampling_rate = None
            self.__file1_raw_data = None
            raise WavImportException('The file "{}/minute_ventilation.wav" has been corrupted and cannot be read.'
                                     .format(self.__input_dir))

        try:
            self.__file2_sampling_rate, self.__file2_raw_data = wavfile.read(self.__input_dir
                                                                             + '/minute_ventilation_adjusted.wav')
        except FileNotFoundError:
            self.__file2_sampling_rate = None
            self.__file2_raw_data = None
            raise WavImportException('ERROR : The file "{}/minute_ventilation_adjusted.wav" can\'t be found.'
                                     .format(self.__input_dir))
        except ValueError:
            self.__file2_sampling_rate = None
            self.__file2_raw_data = None
            raise WavImportException('The file "{}/minute_ventilation_adjusted.wav" has been corrupted and cannot '
                                     'be read.'.format(self.__input_dir))

        if not self.__file1_sampling_rate and not self.__file2_sampling_rate:
            raise WavImportException('The MinuteVentilation Object can\'t be initialized because all the related '
                                     'files are missing or corrupted.')

        if self.__file1_sampling_rate:
            self.nrecords = self.__file1_raw_data.size
            self.duration = self.__file1_raw_data.size / self.__file1_sampling_rate
        else:
            self.nrecords = self.__file2_raw_data.size
            self.duration = self.__file2_raw_data.size / self.__file2_sampling_rate
        self.minute_ventilation = {}
        self.minute_ventilation_quality = {}
        self.__standardize()

    def __standardize(self):
        """
        Standardize the imported data and add the timecode.
        """
        timecode = datetime(1970, 1, 1, 0, 0, 0, 0)
        delta = timedelta(microseconds=(1 / self.__file1_sampling_rate) * 1000000)

        if self.__file1_sampling_rate:
            for record in self.__file1_raw_data:
                self.minute_ventilation[timecode] = record
                timecode = timecode + delta
        timecode = datetime(1970, 1, 1, 0, 0, 0, 0)
        if self.__file2_sampling_rate:
            for record in self.__file2_raw_data:
                self.minute_ventilation_quality[timecode] = record
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
        Export the minute ventilation and breathing_rate_quality to a CSV file.
        """
        # Create the directory if needed
        if not os.path.isdir(self.__output_dir):
            os.mkdir(self.__output_dir)
            print('Create the output directory : "' + self.__output_dir + '".')

        # Generate the CSV
        with open(self.__output_dir + '/minute_ventilation.csv', 'w', newline='') as csvfile:
            filewriter = csv.writer(csvfile, dialect='excel')
            filewriter.writerow(['TimeCode', 'MinuteVentilation(mL/min)', 'MinuteVentilationAdjusted(mL/min)'])
            if self.minute_ventilation:
                for timecode in self.minute_ventilation.keys():
                    filewriter.writerow([timecode.strftime('%H:%M:%S:') + str(int(timecode.microsecond / 1000)),
                                         self.minute_ventilation.get(timecode), self.minute_ventilation_quality.get(timecode)])
            else:
                for timecode in self.minute_ventilation_quality.keys():
                    filewriter.writerow([timecode.strftime('%H:%M:%S:') + str(int(timecode.microsecond / 1000)),
                                         self.minute_ventilation.get(timecode), self.minute_ventilation_quality.get(timecode)])