import os
from termcolor import colored
from .BreathingRate import BreathingRate
from .BreathingRateQuality import BreathingRateQuality
from .Inspiration import Inspiration
from .Expiration import Expiration
from .MinuteVentilation import MinuteVentilation
from .Respiration import Respiration
from .TidalVolume import TidalVolume
from .exception import WavImportException

class Breathing:

    def __init__(self, input_path, output_path):
        self.__input_path = input_path
        self.__output_path = output_path + '/standardize'

        # Create the directory if needed
        if not os.path.isdir(self.__output_path):
            os.mkdir(self.__output_path)
            print('Create the output directory : "' + self.__output_path + '".')
        self.__output_path += '/breathing'
        if not os.path.isdir(self.__output_path):
            os.mkdir(self.__output_path)
            print('Create the output directory : "' + self.__output_path + '".')

        # Init the related objects
        try:
            self.__breathing_rate = BreathingRate(self.__input_path, self.__output_path)
        except WavImportException as error:
            self.__breathing_rate = None
            print(colored(error.args, 'red'))
        try:
            self.__breathing_rate_quality = BreathingRateQuality(self.__input_path, self.__output_path)
        except WavImportException as error:
            self.__breathing_rate_quality = None
            print(colored(error.args, 'red'))
        try:
            self.__inspiration = Inspiration(self.__input_path, self.__output_path)
        except FileExistsError as error:
            self.__inspiration = None
            print(colored('\nERROR : The file "' + error.filename + '" can\'t be found.', 'red'))
        try:
            self.__expiration = Expiration(self.__input_path, self.__output_path)
        except FileExistsError as error:
            self.__expiration = None
            print(colored('\nERROR : The file "' + error.filename + '" can\'t be found.', 'red'))
        try:
            self.__minute_ventilation = MinuteVentilation(self.__input_path, self.__output_path)
        except WavImportException as error:
            self.__minute_ventilation = None
            print(colored(error.args, 'red'))
        try:
            self.__respiration = Respiration(self.__input_path, self.__output_path)
        except WavImportException as error:
            self.__respiration = None
            print(colored(error.args, 'red'))
        try:
            self.__tidal_volume = TidalVolume(self.__input_path, self.__output_path)
        except WavImportException as  error:
            self.__tidal_volume = None
            print(colored(error.args, 'red'))

        print(colored('The breathing related data are imported.', 'green'))


    def export_all(self):
        if self.__breathing_rate:
            self.__breathing_rate.export_csv()
        if self.__breathing_rate_quality:
            self.__breathing_rate_quality.export_csv()
        if self.__expiration:
            self.__expiration.export_csv()
        if self.__inspiration:
            self.__inspiration.export_csv()
        if self.__minute_ventilation:
            self.__minute_ventilation.export_csv()
        if self.__respiration:
            self.__respiration.export_csv()
        if self.__tidal_volume:
            self.__tidal_volume.export_csv()
        print(colored('The breathing related data are exported in csv in the folder '
                      + self.__output_path + '.', 'green'))