import csv
import os
from datetime import datetime
from datetime import timedelta

from scipy.io import wavfile

from hexoskin.standardize.exception.WavImportException import WavImportException


class HearRate:
    """
    Object that represent the heart rate data of the test subject.

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
        The amount of records for the heart rate.
    duration: int
        The duration of the records.
    heart_rate: dict
        The heart rate data as {timecode, record}.
    heart_rate_quality: dict
        The heart rate quality data as {timecode, record}.

    Notes
    -----
        * Heart Rate :*
            Frequency: 1 Hz
            Source data: rrintervalstatus and rrinterval which are based on ecg
            Method of calculation:
                On a QRS detection, if the ECG_STATUS_UNRELIABLE_RR is set to off, the HR is put in the 32 HR buffer. Then the HR is calculated as the average on the last 16 HR.
                On initialisation HR is set to 70 BPM.
            Quality score: heartratestatus
            Average: last 16 beats
            Valid range: 30 to 220 BPM.
                Range is defined by the limits fixed on rrintervalstatus
            Value on initialisation: 70 BPM
            Behavior on invalid detection: keep value of last valid HR
            Unit: BPM

    """

    def __init__(self, input_dir, output_dir):
        self.__input_dir = input_dir
        self.__output_dir = output_dir

        # Try to import the data from a specific WAV file
        try:
            self.__file1_sampling_rate, self.__file1_raw_data = wavfile.read(self.__input_dir + '/heart_rate.wav')
        except FileNotFoundError:
            self.__file1_sampling_rate = None
            self.__file1_raw_data = None
            raise WavImportException('ERROR : The file "{}/heart_rate.wav" can\'t be found.'
                                     .format(self.__input_dir))
        except ValueError:
            self.__file1_sampling_rate = None
            self.__file1_raw_data = None
            raise WavImportException('The file "{]/heart_rate.wav" has been corrupted and cannot be read.'
                                     .format(self.__input_dir))

        try:
            self.__file2_sampling_rate, self.__file2_raw_data = wavfile.read(self.__input_dir
                                                                             + '/heart_rate_quality.wav')
        except FileNotFoundError:
            self.__file2_sampling_rate = None
            self.__file2_raw_data = None
            raise WavImportException('ERROR : The file "{}/heart_rate_quality.wav" can\'t be found.'
                                     .format(self.__input_dir))
        except ValueError:
            self.__file2_sampling_rate = None
            self.__file2_raw_data = None
            raise WavImportException('The file "{}/heart_rate_quality.wav" has been corrupted and cannot be read.'
                                     .format(self.__input_dir))

        if not self.__file1_sampling_rate and not self.__file2_sampling_rate:
            raise WavImportException('The Heart Rate Object can\'t be initialized because all the related'
                                     'files are missing or corrupted.')

        if self.__file1_sampling_rate:
            self.nrecords = self.__file1_raw_data.size
            self.duration = self.__file1_raw_data.size / self.__file1_sampling_rate
        else:
            self.nrecords = self.__file2_raw_data.size
            self.duration = self.__file2_raw_data.size / self.__file2_sampling_rate
        self.heart_rate = {}
        self.heart_rate_quality = {}
        self.__standardize()

    def __standardize(self):
        """
        Standardize the imported data and add the timecode.
        """
        timecode = datetime(1970, 1, 1, 0, 0, 0, 0)
        delta = timedelta(microseconds=(1 / self.__file1_sampling_rate) * 1000000)
        if self.__file1_sampling_rate:
            for record in self.__file1_raw_data:
                self.heart_rate[timecode] = record
                timecode = timecode + delta

        timecode = datetime(1970, 1, 1, 0, 0, 0, 0)
        if self.__file2_sampling_rate:
            for record in self.__file2_raw_data:
                self.heart_rate_quality[timecode] = record
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
        with open(self.__output_dir + '/heart_rate.csv', 'w', newline='') as csvfile:
            filewriter = csv.writer(csvfile, dialect='excel')
            filewriter.writerow(['TimeCode', 'HearRate(BPM)', 'Quality'])
            if self.heart_rate:
                for timecode in self.heart_rate.keys():
                    filewriter.writerow(
                        [timecode.strftime('%H:%M:%S:') + str(int(timecode.microsecond / 1000)),
                         self.heart_rate.get(timecode), self.heart_rate_quality.get(timecode)])
            else:
                for timecode in self.heart_rate_quality.keys():
                    filewriter.writerow(
                        [timecode.strftime('%H:%M:%S:') + str(int(timecode.microsecond / 1000)),
                         self.heart_rate.get(timecode), self.heart_rate_quality.get(timecode)])
