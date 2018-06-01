# -*- coding: utf-8 -*-
import os

from termcolor import colored

from hexoskin.standardize.exception import WavImportException
from hexoskin.standardize.exception.CsvImportException import CsvImportException
from .BreathingRate import BreathingRate
from .Expiration import Expiration
from .Inspiration import Inspiration
from .MinuteVentilation import MinuteVentilation
from .Respiration import Respiration
from .TidalVolume import TidalVolume


class Breathing:
    """
    Object importing and standardizing all the data related to the breathing.

    Parameters
    ----------
        input_dir : str
            The path of the directory where are located the files to import.
        output_dir : str
            The path of the directory where the output fill will be generated.
            The final output_dir is defined by : output_dir + '/breathing'.

    Attributes
    ----------
        __input_dir : str
            The path of the directory where are located the files to import.
        __output_dir : str
            The path of the directory where the output fill will be generated.
        breathing_rate : BreathingRate
            Instance of the BreathingRate object
            None if the object initialization have failed.
        inspiration : Inspiration
            Instance of the Inspiration object
            None if the object initialization have failed.
        expiration : Expiration
            Instance of the Expiration object
            None if the object initialization have failed.
        minute_ventilation : MinuteVentilation
            Instance of the MinuteVentilation object
            None if the object initialization have failed.
        respiration : Respiration
            Instance of the Respiration object
            None if the object initialization have failed.
        tidal_volume : TidalVolume
            Instance of the TidalVolume object
            None if the object initialization have failed.
    """

    def __init__(self, input_dir: str, output_dir: str):
        self.__input_dir = input_dir
        self.__output_dir = output_dir + os.path.sep + 'standardize'

        # Create the output directory if needed
        if not os.path.isdir(self.__output_dir):
            os.mkdir(self.__output_dir)
            print('Create the output directory : "{}".'.format(self.__output_dir))
        self.__output_dir += os.path.sep + 'breathing'
        if not os.path.isdir(self.__output_dir):
            os.mkdir(self.__output_dir)
            print('Create the output directory : "{}".'.format(self.__output_dir))

        # Init the related objects
        try:
            self.breathing_rate = BreathingRate(self.__input_dir, self.__output_dir)
        except WavImportException as error:
            self.breathing_rate = None
            print(colored(error.args[0], 'red'))

        try:
            self.inspiration = Inspiration(self.__input_dir, self.__output_dir)
        except CsvImportException as error:
            self.inspiration = None
            print(colored(error.args[0], 'red'))

        try:
            self.expiration = Expiration(self.__input_dir, self.__output_dir)
        except CsvImportException as error:
            self.expiration = None
            print(colored(error.args[0], 'red'))

        try:
            self.minute_ventilation = MinuteVentilation(self.__input_dir, self.__output_dir)
        except WavImportException as error:
            self.minute_ventilation = None
            print(colored(error.args[0], 'red'))

        try:
            self.respiration = Respiration(self.__input_dir, self.__output_dir)
        except WavImportException as error:
            self.respiration = None
            print(colored(error.args[0], 'red'))

        try:
            self.tidal_volume = TidalVolume(self.__input_dir, self.__output_dir)
        except WavImportException as error:
            self.tidal_volume = None
            print(colored(error.args[0], 'red'))

        print(colored('The breathing related data are imported.', 'green'))

    def update_output_dir(self, dir_path):
        if self.breathing_rate:
            self.breathing_rate.set_output_dir(dir_path)

        if self.expiration:
            self.expiration.set_output_dir(dir_path)

        if self.inspiration:
            self.inspiration.set_output_dir(dir_path)

        if self.minute_ventilation:
            self.minute_ventilation.set_output_dir(dir_path)

        if self.respiration:
            self.respiration.set_output_dir(dir_path)

        if self.tidal_volume:
            self.tidal_volume.set_output_dir(dir_path)


    def export_all_csv(self):
        """
        Export the standardized data of the related objects to a CSV file.
        """
        if self.breathing_rate:
            self.breathing_rate.export_csv()

        if self.expiration:
            self.expiration.export_csv()

        if self.inspiration:
            self.inspiration.export_csv()

        if self.minute_ventilation:
            self.minute_ventilation.export_csv()

        if self.respiration:
            self.respiration.export_csv()

        if self.tidal_volume:
            self.tidal_volume.export_csv()
        print(colored('The breathing related data are exported in csv in the folder "{}".'.format(self.__output_dir)
                      , 'green'))
