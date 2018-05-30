import csv
import os
from datetime import datetime
from datetime import timedelta

from scipy.io import wavfile

from hexoskin.standardize.exception.WavImportException import WavImportException


class Respiration:
    """
    Object that represent the respiration data of the test subject.

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
        The amount of records for the respiration.
    duration: int
        The duration of the records.
    respiration_abdominal: dict
        The respiration_abdominal data as {timecode, record}
    respiration_thoracic: dict
        The respiration_thoracic data as {timecode, record}

    Notes
    -----
        *Respiration :*
            Frequency: 128 Hz
            Raw data (oscillation count in 1/128s)
            Resolution LSB = 128 Hz. i.e. 1 count in 1/128s
            Estimated resolution 8 mL
            Unit: mL
            Unit (binary download): NA



    """
    def __init__(self, input_dir, output_dir):
        self.__input_dir = input_dir
        self.__output_dir = output_dir

        # Try to import the data from a specific WAV file
        try:
            self.__file1_sampling_rate, self.__file1_raw_data = wavfile.read(self.__input_dir
                                                                             + '/respiration_abdominal.wav')
        except FileNotFoundError:
            self.__file1_sampling_rate = None
            self.__file1_raw_data = None
            raise WavImportException('ERROR : The file "' + self.__input_dir + '/respiration_abdominal.wav'
                                     + '" can\'t be found.')
        except ValueError:
            self.__file1_sampling_rate = None
            self.__file1_raw_data = None
            raise WavImportException('The file "' + self.__input_dir + '/respiration_abdominal.wav'
                                     + '" has been corrupted and cannot be read.')

        try:
            self.__file2_sampling_rate, self.__file2_raw_data = wavfile.read(self.__input_dir
                                                                             + '/respiration_thoracic.wav')
        except FileNotFoundError:
            self.__file2_sampling_rate = None
            self.__file2_raw_data = None
            raise WavImportException('ERROR : The file "' + self.__input_dir + '/respiration_thoracic.wav'
                                     + '" can\'t be found.')
        except ValueError:
            self.__file2_sampling_rate = None
            self.__file2_raw_data = None
            raise WavImportException('The file "' + self.__input_dir + '/respiration_thoracic.wav'
                                     + '" has been corrupted and cannot be read.')

        if not self.__file1_sampling_rate and not self.__file2_sampling_rate:
            raise WavImportException('The Respiration Object can\'t be initialized because all the related'
                                     'files are missing or corrupted.')

        if self.__file1_sampling_rate:
            self.nrecords = self.__file1_raw_data.size
            self.duration = self.__file1_raw_data.size / self.__file1_sampling_rate
        else:
            self.nrecords = self.__file2_raw_data.size
            self.duration = self.__file2_raw_data.size / self.__file2_sampling_rate
        self.respiration_abdominal = {}
        self.respiration_thoracic = {}
        self.__standardize()

    def __standardize(self):
        """
        Standardize the imported data and add the timecode.
        """
        timecode = datetime(1970, 1, 1, 0, 0, 0, 0)
        delta = timedelta(microseconds=(1 / self.__file1_sampling_rate) * 1000000)
        if self.__file1_sampling_rate:
            for record in self.__file1_raw_data:
                self.respiration_abdominal[timecode.strftime('%H:%M:%S:%f')] = record
                timecode = timecode + delta

        timecode = datetime(1970, 1, 1, 0, 0, 0, 0)
        if self.__file2_sampling_rate:
            for record in self.__file2_raw_data:
                self.respiration_thoracic[timecode.strftime('%H:%M:%S:%f')] = record
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
        Export the respiration_abdominal and respiration_thoracic_quality to a CSV file.
        """
        # Create the directory if needed
        if not os.path.isdir(self.__output_dir):
            os.mkdir(self.__output_dir)
            print('Create the output directory : "' + self.__output_dir + '".')

        # Generate the CSV
        with open(self.__output_dir + '/respiration.csv', 'w', newline='') as csvfile:
            filewriter = csv.writer(csvfile, dialect='excel')
            filewriter.writerow(['TimeCode', 'RespirationAbdominal(mL)', 'RespirationThoracic(mL)'])
            if self.respiration_abdominal:
                for timecode in self.respiration_abdominal.keys():
                    filewriter.writerow(
                        [timecode, self.respiration_abdominal.get(timecode), self.respiration_thoracic.get(timecode)])
            else:
                for timecode in self.respiration_thoracic.keys():
                    filewriter.writerow(
                        [timecode, self.respiration_abdominal.get(timecode), self.respiration_thoracic.get(timecode)])
