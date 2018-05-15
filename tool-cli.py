#!/usr/bin/python3
import getopt
import os
import sys

from hexoskin.standardize.breathing import Breathing
from hexoskin.standardize.cardiology import Cardiology
from hexoskin.standardize.moves import Moves


def main(argv):
    # Define the default directories
    input_dir = 'input-data'
    output_dir = 'output-data'


    # Try to get the parameters
    try:
        opts, args = getopt.getopt(argv, "hi:o:", ["idir=", "odir="])
        for opt, arg in opts:
            if opt == '-h':
                print_help()
                sys.exit()
            elif opt in ("-i", "--ifile"):
                input_dir = arg
            elif opt in ("-o", "--ofile"):
                output_dir = arg
    except getopt.GetoptError:
        print_help()

    # Get the absolute path of each dir
    input_dir = os.path.abspath(input_dir)
    output_dir = os.path.abspath(output_dir)

    # Create the directories if needed
    if not os.path.isdir(input_dir):
        os.mkdir(input_dir)
        print('Create the directory : "' + input_dir + '".')
    if not os.path.isdir(output_dir):
        os.mkdir(output_dir)
        print('Create the directory : "' + output_dir + '".')

    print('\nInput file is "' + input_dir + '"')
    print('Output file is "' + output_dir + '"\n')
    standardize_data(input_dir, output_dir)
    exit()


def print_help():
    print(
          "usage: tool-cli.py [-i <path> ] [-o <path>]\n" +
          "\t-i : Input directory where the tool will find the raw data of the Hexoskin device\n" +
          "\t     DEFAULT_DIR : ./input-data\n" +
          "\t-o : Output directory where the tool will export the data\n" +
          "\t     DEFAULT_DIR : ./output-data"
          )
    return


def standardize_data(input_path, output_path):
    moves = Moves(input_path, output_path)
    breathing = Breathing(input_path, output_path)
    heart_rate = Cardiology(input_path, output_path)
    moves.export_all()
    breathing.export_all()
    heart_rate.export_all()



if __name__ == "__main__":
    main(sys.argv[1:])