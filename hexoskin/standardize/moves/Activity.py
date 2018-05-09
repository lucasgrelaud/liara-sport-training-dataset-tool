import os
import csv
from termcolor import colored
from datetime import datetime
from datetime import timedelta
from scipy.io import wavfile
from .exception.WavImportException import WavImportException

class Activity:
    """Class which represent the user activity (accelerometer intensity vector)"""
    def __init__(self, input_path, output_path):
        self.file_path = input_path + '/activity.wav'
        self.output_path = output_path

        # Try to import the data from a specific WAV file
        try:
            self.rate, self.raw_data = wavfile.read(self.file_path)
        except FileNotFoundError:
            raise WavImportException('\nERROR : The file "' + self.file_path + '" can\'t be found.')
        except ValueError:
            raise WavImportException('The file "' + self.file_path + '" has been corrupted and cannot be read.')

        print(colored('The activity data are fully imported.', 'green'))

        self.nrecords = self.raw_data.size
        self.time = self.raw_data.size / self.rate
        self.data = {}
        self.add_timecode()

    def get_data(self):
        return self.data

    def print_result(self):
        """
            Print the metadata of the axis record.
        """
        print('Sample rate: ', self.rate)
        print('Records: ', self.raw_data.size)
        print('Duration (seconds): ', self.time)

    def add_timecode(self):
        """
            Generate the records timecode based on the sample rate and
            the recording duration
        """
        timecode = datetime(1970, 1, 1, 0, 0, 0, 0)
        delta = timedelta(microseconds=(1 / self.rate) * 1000000)

        for record in self.raw_data:
            self.data[timecode.strftime('%H:%M:%S:%f')] = record
            timecode = timecode + delta

    def export_csv(self):
        # Create the directory if needed
        if not os.path.isdir(self.output_path):
            os.mkdir(self.output_path)
            print('Create the output directory : "' + self.output_path + '".')

        # Generate the CSV
        with open(self.output_path + '/activity.csv', 'w', newline='') as csvfile:
            spamwriter = csv.writer(csvfile, dialect='excel')
            spamwriter.writerow(['TimeCode', 'Activity'])
            for timecode in self.data.keys():
                spamwriter.writerow([timecode, self.data[timecode]])
