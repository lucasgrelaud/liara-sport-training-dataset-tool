import csv
import os
from datetime import datetime

from hexoskin.standardize.exception.CsvImportException import CsvImportException


class RRInterval:
    """
       Object that represent the RR interval data of the test subject.

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
           The amount of records for the rr interval.
       RR_interval: dict
           The RR Interval data as {timecode, record}
       RR_interval_quality: dict
           The RR Interval quality data as {timecode, record}

       Notes
       -----
           *RR Interval :*
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
        self.RR_interval = {}
        self.RR_interval_quality = {}

        # Import the old CSV
        try:
            with open(self.__input_dir + '/RR_interval.csv', newline='') as csvfile:
                filereader = csv.reader(csvfile, dialect='excel')
                filereader.__next__()
                for row in filereader:
                    timecode = datetime.utcfromtimestamp(float(row[0]))
                    self.RR_interval[timecode.strftime('%H:%M:%S:%f')] = row[1]
        except FileNotFoundError:
            raise CsvImportException('ERROR : The file "{}/RR_interval.csv" can\'t be found.'
                                     .format(self.__input_dir))
        # Import the old CSV
        try:
            with open(self.__input_dir + '/RR_interval_quality.csv', newline='') as csvfile:
                filereader = csv.reader(csvfile, dialect='excel')
                filereader.__next__()
                for row in filereader:
                    timecode = datetime.utcfromtimestamp(float(row[0]))
                    self.RR_interval_quality[timecode.strftime('%H:%M:%S:%f')] = row[1]
        except FileNotFoundError:
            raise CsvImportException('ERROR : The file "{}/RR_interval_quality.csv" can\'t be found.'
                                     .format(self.__input_dir))

    def export_csv(self):
        """
        Export the breathing_rate and breathing_rate_quality to a CSV file.
        """
        # Create the directory if needed
        if not os.path.isdir(self.__output_dir):
            os.mkdir(self.__output_dir)
            print('Create the output directory : "' + self.__output_dir + '".')

        # Generate the CSV
        with open(self.__output_dir + '/RR_interval.csv', 'w', newline='') as csvfile:
            filewriter = csv.writer(csvfile, dialect='excel')
            filewriter.writerow(['TimeCode', 'RRInterval(sec)', 'Quality'])
            for timecode in self.RR_interval.keys():
                filewriter.writerow([timecode, self.RR_interval.get(timecode), self.RR_interval_quality.get(timecode)])
