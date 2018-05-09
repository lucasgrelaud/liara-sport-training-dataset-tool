import os
from .Accelerometer import Accelerometer
from .Activity import Activity
from .Cadence import Cadence


class Moves:

    def __init__(self, input_path, output_path):
        self.__input_path = input_path
        self.__output_path = output_path + '/standardize'

        # Create the directory if needed
        if not os.path.isdir(self.__output_path):
            os.mkdir(self.__output_path)
            print('Create the output directory : "' + self.__output_path + '".')
        self.__output_path += '/moves'
        if not os.path.isdir(self.__output_path):
            os.mkdir(self.__output_path)
            print('Create the output directory : "' + self.__output_path + '".')

        # Init the related objects
        self.__accelerometer = Accelerometer(self.__input_path, self.__output_path)
        self.__activity = Activity(self.__input_path, self.__output_path)
        self.__cadence = Cadence(self.__input_path, self.__output_path)

    def export_all(self):
        self.__accelerometer.export_csv()
        self.__activity.export_csv()
        self.__cadence.export_csv()
