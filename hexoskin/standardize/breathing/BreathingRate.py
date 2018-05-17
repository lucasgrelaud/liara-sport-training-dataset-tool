import csv
import os
from datetime import datetime
from datetime import timedelta

from scipy.io import wavfile

from .exception.WavImportException import WavImportException


class BreathingRate:

    def __init__(self, input_path, output_path):
        self.__file_path = input_path
        self.__output_path = output_path

        # Try to import the data from a specific WAV file
        try:
            self.__rate, self.__raw_data = wavfile.read(self.__file_path + '/breathing_rate.wav')
        except FileNotFoundError:
            raise WavImportException('ERROR : The file "' + self.__file_path + '/breathing_rate.wav'
                                     + '" can\'t be found.')
        except ValueError:
            raise WavImportException('The file "' + self.__file_path + '/breathing_rate.wav'
                                     + '" has been corrupted and cannot be read.')

        try:
            self.__rate2, self.__raw_data2 = wavfile.read(self.__file_path + '/breathing_rate_quality.wav')
        except FileNotFoundError:
            raise WavImportException('ERROR : The file "' + self.__file_path + '/breathing_rate_quality.wav'
                                     + '" can\'t be found.')
        except ValueError:
            raise WavImportException('The file "' + self.__file_path + '/breathing_rate_quality.wav'
                                     + '" has been corrupted and cannot be read.')

        if not self.__rate and not self.__rate2:
            raise WavImportException('The BreathingRate Object can\'t be initialized because all the related '
                                     'files are missing or corrupted.')

        if self.__rate:
            self.__nrecords = self.__raw_data.size
            self.__time = self.__raw_data.size / self.__rate
        else:
            self.__nrecords = self.__raw_data2.size
            self.__time = self.__raw_data2.size / self.__rate2
        self.__data = {}
        self.__data2 = {}
        self.__add_timecode()

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
                self.__data[timecode.strftime('%H:%M:%S:%f')] = record
                timecode = timecode + delta
        timecode = datetime(1970, 1, 1, 0, 0, 0, 0)
        if self.__rate2:
            for record in self.__raw_data2:
                self.__data2[timecode.strftime('%H:%M:%S:%f')] = record
                timecode = timecode + delta

    def export_csv(self):
        # Create the directory if needed
        if not os.path.isdir(self.__output_path):
            os.mkdir(self.__output_path)
            print('Create the output directory : "' + self.__output_path + '".')

        # Generate the CSV
        with open(self.__output_path + '/breathing_rate.csv', 'w', newline='') as csvfile:
            filewriter = csv.writer(csvfile, dialect='excel')
            filewriter.writerow(['TimeCode', 'BreathingRate(RPM)', 'Quality'])
            if self.__data:
                for timecode in self.__data.keys():
                    filewriter.writerow([timecode, self.__data.get(timecode), self.__data2.get(timecode)])
            else:
                for timecode in self.__data2.keys():
                    filewriter.writerow([timecode, self.__data.get(timecode), self.__data2.get(timecode)])