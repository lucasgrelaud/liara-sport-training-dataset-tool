import os
from termcolor import colored
from .Accelerometer import Accelerometer
from .Activity import Activity
from .Cadence import Cadence
from .DevicePosition import DevicePosition
from .Step import Step
from .exception import WavImportException


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
        try:
            self.__accelerometer = Accelerometer(self.__input_path, self.__output_path)
        except WavImportException as error:
            self.__accelerometer = None
            print(colored(error.args, 'red'))
        try:
            self.__activity = Activity(self.__input_path, self.__output_path)
        except WavImportException as error:
            self.__activity = None
            print(colored(error.args, 'red'))
        try:
            self.__cadence = Cadence(self.__input_path, self.__output_path)
        except WavImportException as error:
            self.__cadence = None
            print(colored(error.args, 'red'))
        try:
            self.__device_position = DevicePosition(self.__input_path, self.__output_path)
        except FileNotFoundError as error:
            self.__device_position = None
            print(colored('\nERROR : The file "' + error.filename + '" can\'t be found.', 'red'))
        try:
            self.__step = Step(self.__input_path, self.__output_path)
        except FileNotFoundError as error:
            self.__step = None
            print(colored('\nERROR : The file "' + error.filename + '" can\'t be found.', 'red'))
        print(colored('The moves related data are imported.', 'green'))

    def export_all(self):
        if self.__accelerometer:
            self.__accelerometer.export_csv()
        if self.__activity:
            self.__activity.export_csv()
        if self.__cadence:
            self.__cadence.export_csv()
        if self.__device_position:
            self.__device_position.export_csv()
        if self.__step:
            self.__step.export_csv()
        print(colored('The moves related data are exported in csv in the folder '
                      + self.__output_path + '.', 'green'))
