import os
import csv
from termcolor import colored
from datetime import datetime
from datetime import timedelta
from scipy.io import wavfile
from .exception.WavImportException import WavImportException


class BreathingRate:

    def __init__(self, input_path, output_path):
        self.__file_path = input_path + '/breathing_rate.wav'
        self.__output_path = output_path

        # Try to import the data from a specific WAV file
        try:
            self.__rate, self.__raw_data = wavfile.read(self.__file_path)
        except FileNotFoundError:
            raise WavImportException('\nERROR : The file "' + self.__file_path + '" can\'t be found.')
        except ValueError:
            raise WavImportException('The file "' + self.__file_path + '" has been corrupted and cannot be read.')

        print(colored('The breathing rate data are fully imported.', 'green'))

        self.__nrecords = self.__raw_data.size
        self.__time = self.__raw_data.size / self.__rate
        self.__data = {}
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

        for record in self.__raw_data:
            self.__data[timecode.strftime('%H:%M:%S:%f')] = record
            timecode = timecode + delta

    def export_csv(self):
        # Create the directory if needed
        if not os.path.isdir(self.__output_path):
            os.mkdir(self.__output_path)
            print('Create the output directory : "' + self.__output_path + '".')

        # Generate the CSV
        with open(self.__output_path + '/breathing_rate.csv', 'w', newline='') as csvfile:
            filewriter = csv.writer(csvfile, dialect='excel')
            filewriter.writerow(['TimeCode', 'BreathingRate(RPM)'])
            for timecode in self.__data.keys():
                filewriter.writerow([timecode, self.__data[timecode]])
