import sys
import os

import data_handling

def main(argv):
    script_dir = os.path.dirname(os.path.realpath(__file__))
    data = data_handling.import_unified_file(script_dir + os.path.sep + 'demo_data' + os.path.sep + 'dataset_without_timecode_and_tag.csv')
    data_handling.generate_timecodes(data, 50)


if __name__ == '__main__':
    main(sys.argv)
