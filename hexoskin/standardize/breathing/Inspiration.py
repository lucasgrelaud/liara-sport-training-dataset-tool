import csv
import os
from datetime import datetime

from hexoskin.standardize.exception.CsvImportException import CsvImportException


class Inspiration:
    """
       Object that represent the inspiration data of the test subject.

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
           The amount of records for the inspiration.
       inspiration : dict
           The breathing_rate data as {timecode, record}

       Notes
       -----
           *Inspiration :*
                   Frequency: Async
                   Method of calculation:
                            The inspiration and expiration are detected on the ponderate sum of the thoracic and
                            abdominal sensor.
                            A history buffer is created which correspond to a memory of =.75 s.
                            At each sample, check if the oldest point is a maximum. If it's the case and if the signal
                            decrease of more than 10 units since the last inspiration, the expiration is saved.
                   Unit: respiration per minute
       """

    def __init__(self, input_dir, output_dir):
        self.__input_dir = input_dir
        self.__output_dir = output_dir
        self.inspiration = {}

        # Import the old CSV
        try:
            with open(self.__input_dir + '/inspiration.csv', newline='') as csvfile:
                filereader = csv.reader(csvfile, dialect='excel')
                filereader.__next__()
                for row in filereader:
                    timecode = datetime.utcfromtimestamp(float(row[0]))
                    self.inspiration[timecode] = row[1]
            self.nrecords = len(self.inspiration)
        except FileNotFoundError:
            raise CsvImportException('ERROR : The file "{}/inspiration.csv" can\'t be found.'
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
        Export the inspiration and breathing_rate_quality to a CSV file.
        """
        # Create the directory if needed
        if not os.path.isdir(self.__output_dir):
            os.mkdir(self.__output_dir)
            print('Create the output directory : "' + self.__output_dir + '".')

        # Generate the CSV
        with open(self.__output_dir + '/inspiration.csv', 'w', newline='') as csvfile:
            filewriter = csv.writer(csvfile, dialect='excel')
            filewriter.writerow(['TimeCode', 'Inspiration'])
            for timecode in self.inspiration.keys():
                filewriter.writerow([timecode.strftime('%H:%M:%S:') + str(int(timecode.microsecond / 1000)),
                                     self.inspiration.get(timecode)])
