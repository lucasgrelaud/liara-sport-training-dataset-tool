import csv
import os
from datetime import datetime

from hexoskin.standardize.exception import CsvImportException


class DevicePosition:
    """
       Object that represent the device position data of the test subject.

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
       nrecords: int
           The amount of records for the device position.
       device_position : dict
           The breathing_rate data as {timecode, record}

       Notes
       -----
           *Inspiration :*
                    Frequency: Async

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

    def __init__(self, input_dir, output_dir):
        self.__input_dir = input_dir
        self.__output_dir = output_dir
        self.device_position = {}

        # Import the old CSV
        try:
            with open(self.__input_dir + '/device_position.csv', newline='') as csvfile:
                filereader = csv.reader(csvfile, dialect='excel')
                filereader.__next__()
                for row in filereader:
                    timecode = datetime.utcfromtimestamp(float(row[0]))
                    key = timecode.strftime('%H:%M:%S:') + str(int(timecode.microsecond / 1000))
                    self.device_position[key] = row[1]
        except FileNotFoundError:
            raise CsvImportException('ERROR : The file "{}/device_position.csv" can\'t be found.'
                                     .format(self.__input_dir))

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
        Export the device position to a CSV file.
        """
        # Create the directory if needed
        if not os.path.isdir(self.__output_dir):
            os.mkdir(self.__output_dir)
            print('Create the output directory : "' + self.__output_dir + '".')

        # Generate the CSV
        with open(self.__output_dir + '/device_position.csv', 'w', newline='') as csvfile:
            filewriter = csv.writer(csvfile, dialect='excel')
            filewriter.writerow(['TimeCode', 'Position'])
            for timecode in self.device_position.keys():
                filewriter.writerow([timecode, self.device_position.get(timecode)])
