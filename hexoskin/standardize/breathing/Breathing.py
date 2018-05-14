import os
from .BreathingRate import BreathingRate
from .BreathingRateQuality import BreathingRateQuality
from .Inspiration import Inspiration
from .Expiration import Expiration

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
        self.__breathing_rate = BreathingRate(self.__input_path, self.__output_path)
        self.__breathing_rate_quality = BreathingRateQuality(self.__input_path, self.__output_path)
        self.__inspiration = Inspiration(self.__input_path, self.__output_path)
        self.__expiration = Expiration(self.__input_path, self.__output_path)

    def export_all(self):
        self.__breathing_rate.export_csv()
        self.__breathing_rate_quality.export_csv()
        self.__inspiration.export_csv()
        self.__expiration.export_csv()
