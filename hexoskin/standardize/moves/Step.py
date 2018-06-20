import csv
import os
from datetime import datetime

from hexoskin.standardize.exception import CsvImportException


class Step:
    """
       Object that represent the step data of the test subject.

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
           The amount of records for the step.
       step : dict
           The breathing_rate data as {timecode, record}

       Notes
       -----
           *Step :*


       """

    def __init__(self, input_dir, output_dir):
        self.__input_dir = input_dir
        self.__output_dir = output_dir
        self.step = {}

        # Import the old CSV
        try:
            with open(self.__input_dir + '/step.csv', newline='') as csvfile:
                filereader = csv.reader(csvfile, dialect='excel')
                filereader.__next__()
                for row in filereader:
                    timecode = datetime.utcfromtimestamp(float(row[0]))
                    self.step[timecode] = row[1]
        except FileNotFoundError:
            raise CsvImportException('ERROR : The file "{}/step.csv" can\'t be found.'
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
        Export the step to a CSV file.
        """
        # Create the directory if needed
        if not os.path.isdir(self.__output_dir):
            os.mkdir(self.__output_dir)
            print('Create the output directory : "' + self.__output_dir + '".')

        # Generate the CSV
        with open(self.__output_dir + '/step.csv', 'w', newline='') as csvfile:
            filewriter = csv.writer(csvfile, dialect='excel')
            filewriter.writerow(['TimeCode', 'Step'])
            for timecode in self.step.keys():
                filewriter.writerow([timecode.strftime('%H:%M:%S:') + str(int(timecode.microsecond / 1000)),
                                     self.step.get(timecode)])
