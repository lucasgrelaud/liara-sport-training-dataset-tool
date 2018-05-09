import os
import csv
from datetime import datetime
from termcolor import colored

class DevicePosition:
    """"
    |Position    |Axis pointing upward  |Device position    |
    |:-----------|:--------------------:|:-----------------:|
    |Position 1  | y                    |Blue LED upward    |
    |Position 2  |-y                    |Blue LED downward  |
    |Position 3  | z                    |Face downward      |
    |Position 4  |-z                    |Face upward        |
    |Position 5  | x                    |Wire downward      |
    |Position 6  |-x                    |Wire upward        |
    |Position 0  |                      |Undefined          |
    """

    def __init__(self, input_path, output_path):
        self.__input_file = input_path + '/device_position.csv'
        self.__output_path = output_path
        self.__data = {}

        # Import the old CSV
        with open(self.__input_file, newline='') as csvfile:
            filereader = csv.reader(csvfile, dialect='excel')
            filereader.__next__()
            for row in filereader:
                timecode = datetime.utcfromtimestamp(float(row[0]))
                self.__data[timecode.strftime('%H:%M:%S:%f')] = row[1]
        print(colored('The device_position data are fully imported.', 'green'))


    def export_csv(self):
        # Create the directory if needed
        if not os.path.isdir(self.__output_path):
            os.mkdir(self.__output_path)
            print('Create the output directory : "' + self.__output_path + '".')

        # Generate the CSV
        with open(self.__output_path + '/device_position.csv', 'w', newline='') as csvfile:
            filewriter = csv.writer(csvfile, dialect='excel')
            filewriter.writerow(['TimeCode', 'Position'])
            for timecode in self.__data.keys():
                filewriter.writerow([timecode, self.__data[timecode]])
