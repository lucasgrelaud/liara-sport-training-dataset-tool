import os

from termcolor import colored

from hexoskin.standardize.exception import CsvImportException
from hexoskin.standardize.exception import WavImportException
from .Accelerometer import Accelerometer
from .Activity import Activity
from .Cadence import Cadence
from .DevicePosition import DevicePosition
from .Step import Step


class Moves:
    """
    Object importing and standardizing all the data related to the movements.

    Parameters
    ----------
        input_dir : str
            The path of the directory where are located the files to import.
        output_dir : str
            The path of the directory where the output fill will be generated.
            The final output_dir is defined by : output_dir + '/cardiology'.

    Attributes
    ----------
        __input_dir : str
            The path of the directory where are located the files to import.
        __output_dir : str
            The path of the directory where the output fill will be generated.
        accelerometer : Accelerometer
            Instance of the Accelerometer object
            None if the object initialization have failed.
        activity : Activity
            Instance of the Activity object
            None if the object initialization have failed.
        cadence : Cadence
            Instance of the Cadence object
            None if the object initialization have failed.
        device_position : DevicePosition
            Instance of the DevicePosition object
            None if the object initialization have failed.
        step : Step
            Instance of the Step object
            None if the object initialization have failed.
    """

    def __init__(self, input_dir, output_dir):
        self.__input_dir = input_dir
        self.__output_dir = output_dir + '/standardize'

        # Create the directory if needed
        if not os.path.isdir(self.__output_dir):
            os.mkdir(self.__output_dir)
            print('Create the output directory : "{}".'.format(self.__output_dir))
        self.__output_dir += '/moves'
        if not os.path.isdir(self.__output_dir):
            os.mkdir(self.__output_dir)
            print('Create the output directory : "{}".'.format(self.__output_dir))

        # Init the related objects
        try:
            self.accelerometer = Accelerometer(self.__input_dir, self.__output_dir)
        except WavImportException as error:
            self.accelerometer = None
            print(colored(error.args[0], 'red'))
        try:
            self.activity = Activity(self.__input_dir, self.__output_dir)
        except WavImportException as error:
            self.activity = None
            print(colored(error.args[0], 'red'))
        try:
            self.cadence = Cadence(self.__input_dir, self.__output_dir)
        except WavImportException as error:
            self.cadence = None
            print(colored(error.args[0], 'red'))
        try:
            self.device_position = DevicePosition(self.__input_dir, self.__output_dir)
        except CsvImportException as error:
            self.device_position = None
            print(colored(error.args[0], 'red'))
        try:
            self.step = Step(self.__input_dir, self.__output_dir)
        except CsvImportException as error:
            self.step = None
            print(colored(error.args[0], 'red'))

        print(colored('The moves related data are imported.', 'green'))

    def export_all(self):
        """
        Export the standardized data of the related objects to a CSV file.
        """
        if self.accelerometer:
            self.accelerometer.export_csv()

        if self.activity:
            self.activity.export_csv()

        if self.cadence:
            self.cadence.export_csv()

        if self.device_position:
            self.device_position.export_csv()

        if self.step:
            self.step.export_csv()

        print(colored('The moves related data are exported in csv in the folder "{}".'.format(self.__output_dir)
                      , 'green'))
