import csv
import os

from termcolor import colored

from hexoskin.standardize.exception import WavImportException
from .AccelerometerAxis import AccelerometerAxis


class Accelerometer:
    """
    Object that represent the Accelerometer data of the test subject.

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
    x_axis : AccelerometerAxis
        The data stored in the file.
    y_axis : AccelerometerAxis
        The data stored in the file.
    z_axis : AccelerometerAxis
        The data stored in the file.

    Notes
    -----
        * Accelerometer *
                Frequency: 64 Hz
                Resolution 3.90625 mG
                Dynamic range +- 16G
                Unit: G
                Unit (binary download): G/256
    """

    def __init__(self, input_dir, output_dir):
        self.__input_dir = input_dir
        self.__output_dir = output_dir

        # Import each axis and set the related attributes
        try:
            self.x_axis = AccelerometerAxis('x', input_dir + "/acceleration_X.wav")
        except WavImportException as exception:
            self.x_axis = None
            print(colored(exception, 'red'))
        try:
            self.y_axis = AccelerometerAxis('y', input_dir + "/acceleration_Y.wav")
        except WavImportException as exception:
            self.y_axis = None
            print(colored(exception, 'red'))
        try:
            self.z_axis = AccelerometerAxis('z', input_dir + "/acceleration_Z.wav")
        except WavImportException as exception:
            self.z_axis = None
            print(colored(exception, 'red'))

        # Test if all the axis has been imported
        if not self.__is_fully_initialized():
            print(colored('WARNING : The accelerometer data are partials', 'yellow'))

    def __is_fully_initialized(self):
        return self.x_axis is not None \
               and self.y_axis is not None \
               and self.z_axis is not None

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
        # Create the directory if needed
        if not os.path.isdir(self.__output_dir):
            os.mkdir(self.__output_dir)
            print('Create the output directory : "' + self.__output_dir + '".')

        # Generate the CSV
        x_data = {}
        y_data = {}
        z_data = {}
        if self.x_axis:
            x_data = self.x_axis.axis
        if self.y_axis:
            y_data = self.y_axis.axis
        if self.z_axis:
            z_data = self.z_axis.axis

        with open(self.__output_dir + '/accelerometer.csv', 'w', newline='') as csvfile:
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
