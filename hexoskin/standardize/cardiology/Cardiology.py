import os

from termcolor import colored

from .ECG import ECG
from .HeartRate import HearRate
from .RRInterval import RRInterval
from .exception import WavImportException


class Cardiology:

    def __init__(self, input_path, output_path):
        self.__input_path = input_path
        self.__output_path = output_path + '/standardize'

        # Create the directory if needed
        if not os.path.isdir(self.__output_path):
            os.mkdir(self.__output_path)
            print('Create the output directory : "' + self.__output_path + '".')
        self.__output_path += '/cardiology'
        if not os.path.isdir(self.__output_path):
            os.mkdir(self.__output_path)
            print('Create the output directory : "' + self.__output_path + '".')

        # Init the related objects
        try:
            self.__ecg = ECG(self.__input_path, self.__output_path)
        except WavImportException as error:
            self.__ecg = None
            print(colored(error.args[0], 'red'))
        try:
            self.__heart_rate = HearRate(self.__input_path, self.__output_path)
        except WavImportException as error:
            self.__heart_rate = None
            print(colored(error.args[0], 'red'))
        try:
            self.__RR_interval = RRInterval(self.__input_path, self.__output_path)
        except WavImportException as error:
            self.__RR_interval = None
            print(colored(error.args[0], 'red'))

        print(colored('The cardiology related data are imported.', 'green'))

    def export_all(self):
        if self.__ecg:
            self.__ecg.export_csv()
        if self.__heart_rate:
            self.__heart_rate.export_csv()
        if self.__RR_interval:
            self.__RR_interval.export_csv()
        print(colored('The cardiology related data are exported in csv in the folder '
                      + self.__output_path + '.', 'green'))
