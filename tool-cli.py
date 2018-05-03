#!/usr/bin/python3
import sys
import getopt
import os

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

    # Create the directories if needed
    if not os.path.isdir(input_dir):
        os.mkdir(input_dir)
        print('Create the directory : "' + input_dir + '".')
    if not os.path.isdir(output_dir):
        os.mkdir(output_dir)
        print('Create the directory : "' + output_dir + '".')

    print('Input file is "' + input_dir + '"')
    print('Output file is "' + output_dir + '"')
    exit()


def print_help():
    print(
          "usage: tool-cli.py [-i <path> ] [-o <path>]\n" +
          "\t-i : Input directory where the tool will find the raw data of the Hexoskin\n" +
          "\t     DEFAULT_DIR : ./input-data\n" +
          "\t-o : Output directory where the tool will export the data\n" +
          "\t     DEFAULT_DIR : ./output-data"
          )
    return


if __name__ == "__main__":
    main(sys.argv[1:])