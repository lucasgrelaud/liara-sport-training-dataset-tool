import csv
import os

from datetime import datetime
from datetime import timedelta

from scipy.io import wavfile

from .exception.WavImportException import WavImportException


class BreathingRate:
    """
    Object that represent the breathing rate data of the test subject.

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
        The amount of records for the breathing_rate.
    duration: int
        The duration of the records.
    breathing_rate: dict
        The breathing_rate data as {timecode, record}
    breathing_rate_quality: dict
        The breathing_rate_quality data as {timecode, record}

    Notes
    -----
        *Breathing Rate :*
                Frequency: 1 Hz
                Average: last 7 respiration cycles
                Valid range: (2 to 60 RPM)
                    If BR > 60: Clip to 60
                    If BR < 2: set to 2
                Unit: respiration per minute

        *Breathing Rate Quality :*
                Frequency: 1Hz
                Bits description:
                    RESP_STATUS_OK (0x00) /!< Resp good quality./
                    RESP_STATUS_NO_A (0x01) /!< Resp channel A (thoracic) is disconnected./
                    RESP_STATUS_NO_B (0x02) /!< Resp channel B (abdominal) is disconnected./
                    RESP_STATUS_BASELINE_A (0x04) /!< Resp A baseline has changed. /
                    RESP_STATUS_BASELINE_B (0x08) /!< Resp B baseline has changed. /
                    RESP_STATUS_NOISY_A (0x10) /!< Resp A has high frequency content. /
                    RESP_STATUS_NOISY_B (0x20) /!< Resp B has high frequency content. /

    """

    def __init__(self, input_dir, output_dir):
        self.__input_dir = input_dir
        self.__output_dir = output_dir

        # Try to import the data from a specific WAV file
        try:
            self.__file1_sampling_rate, self.__file1_raw_data = wavfile.read(self.__input_dir + '/breathing_rate.wav')
        except FileNotFoundError:
            raise WavImportException('ERROR : The file "{}/breathing_rate.wav" can\'t be found.'
                                     .format(self.__input_dir))
        except ValueError:
            raise WavImportException('The file "{}/breathing_rate.wav" has been corrupted and cannot be read.'
                                     .format(self.__input_dir))

        try:
            self.__file2_sampling_rate, self.__file2_raw_data = wavfile.read(self.__input_dir
                                                                             + '/breathing_rate_quality.wav')
        except FileNotFoundError:
            raise WavImportException('ERROR : The file "{}/breathing_rate_quality.wav" can\'t be found.'
                                     .format(self.__input_dir))
        except ValueError:
            raise WavImportException('The file "/breathing_rate_quality.wav" has been corrupted and cannot be read.'
                                     .format(self.__input_dir))

        # Test if a lest one file have been loaded
        if not self.__file1_sampling_rate and not self.__file2_sampling_rate:
            raise WavImportException('The BreathingRate Object can\'t be initialized because all the related '
                                     'files are missing or corrupted.')

        if self.__file1_sampling_rate:
            self.nrecords = self.__file1_raw_data.size
            self.duration = self.__file1_raw_data.size / self.__file1_sampling_rate
        else:
            self.nrecords = self.__file2_raw_data.size
            self.duration = self.__file2_raw_data.size / self.__file2_sampling_rate
        self.breathing_rate = {}
        self.breathing_rate_quality = {}
        self.__standardize()

    def __standardize(self):
        """
        Standardize the imported data and add the timecode.
        """
        timecode = datetime(1970, 1, 1, 0, 0, 0, 0)
        delta = timedelta(microseconds=(1 / self.__file1_sampling_rate) * 1000000)

        if self.__file1_sampling_rate:
            for record in self.__file1_raw_data:
                self.breathing_rate[timecode.strftime('%H:%M:%S:%f')] = record
                timecode = timecode + delta
        timecode = datetime(1970, 1, 1, 0, 0, 0, 0)
        if self.__file2_sampling_rate:
            for record in self.__file2_raw_data:
                self.breathing_rate_quality[timecode.strftime('%H:%M:%S:%f')] = record
                timecode = timecode + delta

    def export_csv(self):
        """
        Export the minute_ventilation and minute_ventilation_quality to a CSV file.
        """
        # Create the directory if needed
        if not os.path.isdir(self.__output_dir):
            os.mkdir(self.__output_dir)
            print('Create the output directory : "' + self.__output_dir + '".')

        # Generate the CSV
        with open(self.__output_dir + '/breathing_rate.csv', 'w', newline='') as csvfile:
            filewriter = csv.writer(csvfile, dialect='excel')
            filewriter.writerow(['TimeCode', 'BreathingRate(RPM)', 'Quality'])
            if self.breathing_rate:
                for timecode in self.breathing_rate.keys():
                    filewriter.writerow(
                        [timecode, self.breathing_rate.get(timecode), self.breathing_rate_quality.get(timecode)])
            else:
                for timecode in self.breathing_rate_quality.keys():
                    filewriter.writerow(
                        [timecode, self.breathing_rate.get(timecode), self.breathing_rate_quality.get(timecode)])
