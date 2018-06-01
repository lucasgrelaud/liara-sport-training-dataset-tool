import csv
import os
from datetime import datetime
from datetime import timedelta

from scipy.io import wavfile

from hexoskin.standardize.exception.CsvImportException import CsvImportException
from hexoskin.standardize.exception.WavImportException import WavImportException


class TidalVolume:
    """
    Object that represent the tidal volume data of the test subject.

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
        The amount of records for the tidal volume.
    duration: int
        The duration of the records.
    tidal_volume: dict
        The tidal_volume data as {timecode, record}
    tidal_volume_quality: dict
        The tidal_volume_quality data as {timecode, record}

    Notes
    -----
        * Tidal Volume :*
                Frequency: 1 Hz
                Unit: mL (mL / inspiration)
                Unit (binary download): mL *13.28



    """
    def __init__(self, input_dir, output_dir):
        self.__input_dir = input_dir
        self.__output_dir = output_dir

        # Try to import the data from a specific WAV file
        try:
            self.__file1_sampling_rate, self.__file1_raw_data = wavfile.read(self.__input_dir + '/tidal_volume.wav')
        except FileNotFoundError:
            self.__file1_sampling_rate = None
            self.__file1_raw_data = None
            raise WavImportException('ERROR : The file "' + self.__input_dir + '/tidal_volume.wav'
                                     + '" can\'t be found.')
        except ValueError:
            self.__file1_sampling_rate = None
            self.__file1_raw_data = None
            raise WavImportException('The file "' + self.__input_dir + '/tidal_volume.wav'
                                     + '" has been corrupted and cannot be read.')

        try:
            self.__file2_sampling_rate, self.__file2_raw_data = wavfile.read(self.__input_dir
                                                                             + '/tidal_volume_adjusted.wav')
        except FileNotFoundError:
            self.__file2_sampling_rate = None
            self.__file2_raw_data = None
            raise WavImportException('ERROR : The file "' + self.__input_dir + '/tidal_volume_adjusted.wav'
                                     + '" can\'t be found.')
        except ValueError:
            self.__file2_sampling_rate = None
            self.__file2_raw_data = None
            raise WavImportException('The file "' + self.__input_dir + '/tidal_volume_adjusted.wav'
                                     + '" has been corrupted and cannot be read.')

        if not self.__file1_sampling_rate and not self.__file2_sampling_rate:
            raise CsvImportException('The TidalVolume Object can\'t be initialized because all the related'
                                     'files are missing or corrupted.')

        if self.__file1_sampling_rate:
            self.nrecords = self.__file1_raw_data.size
            self.duration = self.__file1_raw_data.size / self.__file1_sampling_rate
        else:
            self.nrecords = self.__file2_raw_data.size
            self.duration = self.__file2_raw_data.size / self.__file2_sampling_rate
        self.tidal_volume = {}
        self.tidal_volume_quality = {}
        self.__standardize()

    def __standardize(self):
        """
        Standardize the imported data and add the timecode.
        """
        timecode = datetime(1970, 1, 1, 0, 0, 0, 0)
        delta = timedelta(microseconds=(1 / self.__file1_sampling_rate) * 1000000)
        if self.__file1_sampling_rate:
            for record in self.__file1_raw_data:
                key = timecode.strftime('%H:%M:%S:') + str(int(timecode.microsecond / 1000))
                self.tidal_volume[key] = record
                timecode = timecode + delta
        timecode = datetime(1970, 1, 1, 0, 0, 0, 0)
        if self.__file2_sampling_rate:
            for record in self.__file2_raw_data:
                key = timecode.strftime('%H:%M:%S:') + str(int(timecode.microsecond / 1000))
                self.tidal_volume_quality[key] = record
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
        Export the tidal_volume and tidal_volume_quality to a CSV file.
        """
        # Create the directory if needed
        if not os.path.isdir(self.__output_dir):
            os.mkdir(self.__output_dir)
            print('Create the output directory : "' + self.__output_dir + '".')

        # Generate the CSV
        with open(self.__output_dir + '/tidal_volume.csv', 'w', newline='') as csvfile:
            filewriter = csv.writer(csvfile, dialect='excel')
            filewriter.writerow(['TimeCode', 'TidalVolume(RPM)', 'TidalVolumeAdjusted(RPM)'])
            if self.tidal_volume:
                for timecode in self.tidal_volume.keys():
                    filewriter.writerow([timecode, self.tidal_volume.get(timecode), self.tidal_volume_quality.get(timecode)])
            else:
                for timecode in self.tidal_volume_quality.keys():
                    filewriter.writerow([timecode, self.tidal_volume.get(timecode), self.tidal_volume_quality.get(timecode)])