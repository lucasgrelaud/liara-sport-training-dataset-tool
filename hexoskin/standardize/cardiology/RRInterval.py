import csv
import os
from datetime import datetime


class RRInterval:

    def __init__(self, input_path, output_path):
        self.__input_file = input_path
        self.__output_path = output_path
        self.__RR_interval = {}
        self.__RR_interval_quality = {}

        # Import the old CSV
        with open(self.__input_file + '/RR_interval.csv', newline='') as csvfile:
            filereader = csv.reader(csvfile, dialect='excel')
            filereader.__next__()
            for row in filereader:
                timecode = datetime.utcfromtimestamp(float(row[0]))
                self.__RR_interval[timecode.strftime('%H:%M:%S:%f')] = row[1]
        # Import the old CSV
        with open(self.__input_file + '/RR_interval_quality.csv', newline='') as csvfile:
            filereader = csv.reader(csvfile, dialect='excel')
            filereader.__next__()
            for row in filereader:
                timecode = datetime.utcfromtimestamp(float(row[0]))
                self.__RR_interval_quality[timecode.strftime('%H:%M:%S:%f')] = row[1]

    def export_csv(self):
        # Create the directory if needed
        if not os.path.isdir(self.__output_path):
            os.mkdir(self.__output_path)
            print('Create the output directory : "' + self.__output_path + '".')

        # Generate the CSV
        with open(self.__output_path + '/RR_interval.csv', 'w', newline='') as csvfile:
            filewriter = csv.writer(csvfile, dialect='excel')
            filewriter.writerow(['TimeCode', 'RRInterval(sec)', 'Quality'])
            for timecode in self.__RR_interval.keys():
                filewriter.writerow([timecode, self.__RR_interval.get(timecode), self.__RR_interval_quality.get(timecode)])
