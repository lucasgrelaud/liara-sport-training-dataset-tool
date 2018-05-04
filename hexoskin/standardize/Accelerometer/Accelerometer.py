from hexoskin.standardize.Accelerometer.AccelerometerAxis import AccelerometerAxis
from hexoskin.standardize.Accelerometer.exception.WavImportException import WavImportException
from termcolor import colored


class Accelerometer:
    """"Class which represent the accelerometer"""

    def __init__(self, input_path, output_path):
        self.dir_path = input_path

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
            self.z_axis.print_result()

        print(self.x_axis.data)

    def is_fully_initialized(self):
        return self.x_axis is not None \
               and self.y_axis is not None \
               and self.z_axis is not None
