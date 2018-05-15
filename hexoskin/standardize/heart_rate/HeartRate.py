import os

from termcolor import colored

from .ECG import ECG
from .exception import WavImportException


class HeartRate:

    def __init__(self, input_path, output_path):
        self.__input_path = input_path
        self.__output_path = output_path + '/standardize'

        # Create the directory if needed
        if not os.path.isdir(self.__output_path):
            os.mkdir(self.__output_path)
            print('Create the output directory : "' + self.__output_path + '".')
        self.__output_path += '/heart_rate'
        if not os.path.isdir(self.__output_path):
            os.mkdir(self.__output_path)
            print('Create the output directory : "' + self.__output_path + '".')

        # Init the related objects
        try:
            self.__ecg = ECG(self.__input_path, self.__output_path)
        except WavImportException as error:
            self.__ = None
            print(colored(error.args, 'red'))

        print(colored('The heart rate related data are imported.', 'green'))

    def export_all(self):
        if self.__ecg:
            self.__ecg.export_csv()
        print(colored('The heart rate related data are exported in csv in the folder '
                      + self.__output_path + '.', 'green'))
