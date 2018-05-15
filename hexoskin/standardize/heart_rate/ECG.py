import csv
import os
from datetime import datetime
from datetime import timedelta

from scipy.io import wavfile

from .exception.DataImportException import DataImportException
from .exception.WavImportException import WavImportException


class ECG:

    def __init__(self, input_path, output_path):
        self.__file_path = input_path
        self.__output_path = output_path

        # Try to import the data from a the first ECG file
        try:
            self.__rate, self.__raw_data = wavfile.read(self.__file_path + '/ECG_I.wav')
        except FileNotFoundError:
            self.__rate = None
            self.__raw_data = None
            raise WavImportException('\nERROR : The file "' + self.__file_path + '/ECG_I.wav'
                                     + '" can\'t be found.')
        except ValueError:
            self.__rate = None
            self.__raw_data = None
            raise WavImportException('The file "' + self.__file_path + '/ECG_I.wav'
                                     + '" has been corrupted and cannot be read.')

        # Try to import the data from a the second ECG file
        try:
            self.__rate2, self.__raw_data2 = wavfile.read(self.__file_path + '/ECG_II.wav')
        except FileNotFoundError:
            self.__rate2 = None
            self.__raw_data2 = None
            raise WavImportException('\nERROR : The file "' + self.__file_path + '/ECG_II.wav'
                                     + '" can\'t be found.')
        except ValueError:
            self.__rate2 = None
            self.__raw_data2 = None
            raise WavImportException('The file "' + self.__file_path + '/ECG_II.wav'
                                     + '" has been corrupted and cannot be read.')

        # Try to import the data from a the third ECG file
        try:
            self.__rate3, self.__raw_data3 = wavfile.read(self.__file_path + '/ECG_III.wav')
        except FileNotFoundError:
            self.__rate3 = None
            self.__raw_data3 = None
            raise WavImportException('\nERROR : The file "' + self.__file_path + '/ECG_III.wav'
                                     + '" can\'t be found.')
        except ValueError:
            self.__rate3 = None
            self.__raw_data3 = None
            raise WavImportException('The file "' + self.__file_path + '/ECG_III.wav'
                                     + '" has been corrupted and cannot be read.')

        # Test if at least one file have been loaded
        if not self.__rate and not self.__rate2 and not self.__rate3:
            raise DataImportException('The ECG Object can\'t be initialized because all the related'
                                      'files are missing or corrupted.')

        if self.__rate:
            self.__nrecords = self.__raw_data.size
            self.__time = self.__raw_data.size / self.__rate
        elif self.__rate2:
            self.__nrecords = self.__raw_data2.size
            self.__time = self.__raw_data2.size / self.__rate2
        else:
            self.__nrecords = self.__raw_data3.size
            self.__time = self.__raw_data3.size / self.__rate3
        self.__ecg1 = {}
        self.__ecg2 = {}
        self.__ecg3 = {}
        self.__add_timecode()

    def get_time(self):
        return self.__time

    def get_nrecords(self):
        return self.__nrecords

    def get_data(self):
        return self.__ecg1

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
                self.__ecg1[timecode.strftime('%H:%M:%S:%f')] = record
                timecode = timecode + delta
        timecode = datetime(1970, 1, 1, 0, 0, 0, 0)
        if self.__rate2:
            for record in self.__raw_data2:
                self.__ecg2[timecode.strftime('%H:%M:%S:%f')] = record
                timecode = timecode + delta
        timecode = datetime(1970, 1, 1, 0, 0, 0, 0)
        if self.__rate3:
            for record in self.__raw_data3:
                self.__ecg3[timecode.strftime('%H:%M:%S:%f')] = record
                timecode = timecode + delta

    def export_csv(self):
        # Create the directory if needed
        if not os.path.isdir(self.__output_path):
            os.mkdir(self.__output_path)
            print('Create the output directory : "' + self.__output_path + '".')

        # Generate the CSV
        with open(self.__output_path + '/ecg.csv', 'w', newline='') as csvfile:
            filewriter = csv.writer(csvfile, dialect='excel')
            filewriter.writerow(['TimeCode', 'ECG_I(mV * 0.0064)', 'ECG_II(mV * 0.0064)', 'ECG_III(mV * 0.0064)'])
            if self.__ecg1:
                for timecode in self.__ecg1.keys():
                    filewriter.writerow(
                        [timecode, self.__ecg1.get(timecode), self.__ecg2.get(timecode), self.__ecg3.get(timecode)])
            elif self.__rate2:
                for timecode in self.__ecg2.keys():
                    filewriter.writerow(
                        [timecode, self.__ecg1.get(timecode), self.__ecg2.get(timecode), self.__ecg3.get(timecode)])
            else:
                for timecode in self.__ecg3.keys():
                    filewriter.writerow(
                        [timecode, self.__ecg1.get(timecode), self.__ecg2.get(timecode), self.__ecg3.get(timecode)])
