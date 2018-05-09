import os
from .Accelerometer import Accelerometer
from .Activity import Activity

class Moves:

    def __init__(self, input_path, output_path):
        self.input_path = input_path
        self.output_path = output_path + '/standardize'

        # Create the directory if needed
        if not os.path.isdir(self.output_path):
            os.mkdir(self.output_path)
            print('Create the output directory : "' + self.output_path + '".')
        self.output_path += '/moves'
        if not os.path.isdir(self.output_path):
            os.mkdir(self.output_path)
            print('Create the output directory : "' + self.output_path + '".')

        # Init the related objects
        self.accelerometer = Accelerometer(self.input_path, self.output_path)
        self.activity = Activity(self.input_path, self.output_path)


    def export_all(self):
        self.accelerometer.export_csv()
        self.activity.export_csv()
