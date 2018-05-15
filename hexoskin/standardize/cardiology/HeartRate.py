import os
import csv

from datetime import datetime
from datetime import timedelta
from scipy.io import wavfile
from .exception.WavImportException import WavImportException
from .exception.DataImportException import DataImportException


class HearRate:

    def __init__(self, input_path, output_path):
        self.__file_path = input_path
        self.__output_path = output_path

        # Try to import the data from a specific WAV file
        try:
            self.__rate, self.__raw_data = wavfile.read(self.__file_path + '/heart_rate.wav')
        except FileNotFoundError:
            self.__rate = None
            self.__raw_data = None
            raise WavImportException('\nERROR : The file "' + self.__file_path + '/heart_rate.wav'
                                     + '" can\'t be found.')
        except ValueError:
            self.__rate = None
            self.__raw_data = None
            raise WavImportException('The file "' + self.__file_path + '/heart_rate.wav'
                                     + '" has been corrupted and cannot be read.')

        try:
            self.__rate2, self.__raw_data2 = wavfile.read(self.__file_path + '/heart_rate_quality.wav')
        except FileNotFoundError:
            self.__rate2 = None
            self.__raw_data2 = None
            raise WavImportException('\nERROR : The file "' + self.__file_path + '/heart_rate_quality.wav'
                                     + '" can\'t be found.')
        except ValueError:
            self.__rate2 = None
            self.__raw_data2 = None
            raise WavImportException('The file "' + self.__file_path + '/heart_rate_quality.wav'
                                     + '" has been corrupted and cannot be read.')

        if not self.__rate and not self.__rate2:
            raise DataImportException('The Heart Rate Object can\'t be initialized because all the related'
                                      'files are missing or corrupted.')

        if self.__rate:
            self.__nrecords = self.__raw_data.size
            self.__time = self.__raw_data.size / self.__rate
        else:
            self.__nrecords = self.__raw_data2.size
            self.__time = self.__raw_data2.size / self.__rate2
        self.__heart_rare = {}
        self.__heart_rate_quality = {}
        self.__add_timecode()

    def get_time(self):
        return self.__time

    def get_nrecords(self):
        return self.__nrecords

    def get_data(self):
        return self.__heart_rare

    def print_result(self):
        """
            Print the metadata of the axis record.
        """
        print('Sample rate: ', self.__rate)
        print('Records: ', self.__raw_data.size)
        print('Duration (seconds): ', self.__time)

    def __add_timecode(self):
        """
            Generate the records timecode based on the sample rate and
            the recording duration
        """
        timecode = datetime(1970, 1, 1, 0, 0, 0, 0)
        delta = timedelta(microseconds=(1 / self.__rate) * 1000000)
        if self.__rate:
            for record in self.__raw_data:
                self.__heart_rare[timecode.strftime('%H:%M:%S:%f')] = record
                timecode = timecode + delta

        timecode = datetime(1970, 1, 1, 0, 0, 0, 0)
        if self.__rate2:
            for record in self.__raw_data2:
                self.__heart_rate_quality[timecode.strftime('%H:%M:%S:%f')] = record
                timecode = timecode + delta

    def export_csv(self):
        # Create the directory if needed
        if not os.path.isdir(self.__output_path):
            os.mkdir(self.__output_path)
            print('Create the output directory : "' + self.__output_path + '".')

        # Generate the CSV
        with open(self.__output_path + '/heart_rate.csv', 'w', newline='') as csvfile:
            filewriter = csv.writer(csvfile, dialect='excel')
            filewriter.writerow(['TimeCode', 'HearRate(BPM)', 'Quality'])
            if self.__heart_rare:
                for timecode in self.__heart_rare.keys():
                    filewriter.writerow(
                        [timecode, self.__heart_rare.get(timecode), self.__heart_rate_quality.get(timecode)])
            else:
                for timecode in self.__heart_rate_quality.keys():
                    filewriter.writerow(
                        [timecode, self.__heart_rare.get(timecode), self.__heart_rate_quality.get(timecode)])
