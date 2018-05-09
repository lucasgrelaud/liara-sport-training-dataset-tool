import os
import csv
from termcolor import colored
from .AccelerometerAxis import AccelerometerAxis
from .exception import WavImportException


class Accelerometer:
    """"Class which represent the accelerometer"""

    def __init__(self, input_path, output_path):
        self.input_path = input_path
        self.output_path = output_path + "/standardize"

        # Import each axis and set the related attributes
        try:
            self.x_axis = AccelerometerAxis('x', input_path + "/acceleration_X.wav")
        except WavImportException as exception:
            self.x_axis = None
            print(colored(exception, 'red'))
        try:
            self.y_axis = AccelerometerAxis('y', input_path + "/acceleration_Y.wav")
        except WavImportException as exception:
            self.y_axis = None
            print(colored(exception, 'red'))
        try:
            self.z_axis = AccelerometerAxis('z', input_path + "/acceleration_Z.wav")
        except WavImportException as exception:
            self.z_axis = None
            print(colored(exception, 'red'))

        # Test if all the axis has been imported
        if not self.is_fully_initialized():
            print(colored('\nWARNING : The accelerometer data are partials', 'yellow'))
        else:
            print(colored('\nThe accelerometer data are fully imported', 'green'))

    def is_fully_initialized(self):
        return self.x_axis is not None \
               and self.y_axis is not None \
               and self.z_axis is not None

    def export_csv(self):
        # Create the directory if needed
        if not os.path.isdir(self.output_path):
            os.mkdir(self.output_path)
            print('Create the output directory : "' + self.output_path + '".')

        # Generate the CSV
        x_data = self.x_axis.get_data()
        y_data = self.y_axis.get_data()
        z_data = self.z_axis.get_data()
        with open(self.output_path + '/accelerometer.csv', 'w', newline='') as csvfile:
            spamwriter = csv.writer(csvfile, dialect='excel')
            spamwriter.writerow(['TimeCode', 'X', 'Y', 'Z'])
            for timecode in x_data.keys():
                spamwriter.writerow([timecode, x_data[timecode], y_data[timecode], z_data[timecode]])