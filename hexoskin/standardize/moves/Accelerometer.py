import os
import csv
from termcolor import colored
from .AccelerometerAxis import AccelerometerAxis
from .exception import WavImportException


class Accelerometer:
    """"Class which represent the accelerometer"""

    def __init__(self, input_path, output_path):
        self.__input_path = input_path
        self.__output_path = output_path

        # Import each axis and set the related attributes
        try:
            self.__x_axis = AccelerometerAxis('x', input_path + "/acceleration_X.wav")
        except WavImportException as exception:
            self.__x_axis = None
            print(colored(exception, 'red'))
        try:
            self.__y_axis = AccelerometerAxis('y', input_path + "/acceleration_Y.wav")
        except WavImportException as exception:
            self.__y_axis = None
            print(colored(exception, 'red'))
        try:
            self.__z_axis = AccelerometerAxis('z', input_path + "/acceleration_Z.wav")
        except WavImportException as exception:
            self.__z_axis = None
            print(colored(exception, 'red'))

        # Test if all the axis has been imported
        if not self.__is_fully_initialized():
            print(colored('\nWARNING : The accelerometer data are partials', 'yellow'))

    def __is_fully_initialized(self):
        return self.__x_axis is not None \
               and self.__y_axis is not None \
               and self.__z_axis is not None

    def export_csv(self):
        # Create the directory if needed
        if not os.path.isdir(self.__output_path):
            os.mkdir(self.__output_path)
            print('Create the output directory : "' + self.__output_path + '".')

        # Generate the CSV
        x_data = {}
        y_data = {}
        z_data = {}
        if self.__x_axis:
            x_data = self.__x_axis.get_data()
        if self.__y_axis:
            y_data = self.__y_axis.get_data()
        if self.__z_axis:
            z_data = self.__z_axis.get_data()

        with open(self.__output_path + '/accelerometer.csv', 'w', newline='') as csvfile:
            filewriter = csv.writer(csvfile, dialect='excel')
            filewriter.writerow(['TimeCode', 'X(G)', 'Y(G)', 'Z(G)'])
            if x_data:
                for timecode in x_data.keys():
                    filewriter.writerow([timecode, x_data.get(timecode), y_data.get(timecode), z_data.get(timecode)])
            elif y_data:
                for timecode in y_data.keys():
                    filewriter.writerow([timecode, x_data.get(timecode), y_data.get(timecode), z_data.get(timecode)])
            else:
                for timecode in z_data.keys():
                    filewriter.writerow([timecode, x_data.get(timecode), y_data.get(timecode), z_data.get(timecode)])
