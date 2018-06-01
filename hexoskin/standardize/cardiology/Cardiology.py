import os

from termcolor import colored

from hexoskin.standardize.exception.CsvImportException import CsvImportException
from hexoskin.standardize.exception.WavImportException import WavImportException
from .ECG import ECG
from .HeartRate import HearRate
from .RRInterval import RRInterval


class Cardiology:
    """
    Object importing and standardizing all the data related to the cardiology.

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
        ecg : ECG
            Instance of the ECG object
            None if the object initialization have failed.
        heart_rate : HearRate
            Instance of the HeartRate object
            None if the object initialization have failed.
        RR_interval : RRInterval
            Instance of the RRInterval object
            None if the object initialization have failed.
    """

    def __init__(self, input_dir, output_dir):
        self.__input_dir = input_dir
        self.__output_dir = output_dir + os.path.sep + 'standardize'

        # Create the directory if needed
        if not os.path.isdir(self.__output_dir):
            os.mkdir(self.__output_dir)
            print('Create the output directory : "{}".'.format(self.__output_dir))
        self.__output_dir += os.path.sep + 'cardiology'
        if not os.path.isdir(self.__output_dir):
            os.mkdir(self.__output_dir)
            print('Create the output directory : "{}".'.format(self.__output_dir))

        # Init the related objects
        try:
            self.ecg = ECG(self.__input_dir, self.__output_dir)
        except WavImportException as error:
            self.ecg = None
            print(colored(error.args[0], 'red'))
        try:
            self.heart_rate = HearRate(self.__input_dir, self.__output_dir)
        except WavImportException as error:
            self.heart_rate = None
            print(colored(error.args[0], 'red'))
        try:
            self.RR_interval = RRInterval(self.__input_dir, self.__output_dir)
        except CsvImportException as error:
            self.RR_interval = None
            print(colored(error.args[0], 'red'))

        print(colored('The cardiology related data are imported.', 'green'))

    def update_output_dir(self, dir_path):
        if self.ecg:
            self.ecg.set_output_dir(dir_path)

        if self.heart_rate:
            self.heart_rate.set_output_dir(dir_path)

        if self.RR_interval:
            self.RR_interval.set_output_dir(dir_path)

    def export_all_csv(self):
        """
        Export the standardized data of the related objects to a CSV file.
        """
        if self.ecg:
            self.ecg.export_csv()

        if self.heart_rate:
            self.heart_rate.export_csv()

        if self.RR_interval:
            self.RR_interval.export_csv()

        print(colored('The cardiology related data are exported in csv in the folder "{}".'.format(self.__output_dir)
                      , 'green'))
