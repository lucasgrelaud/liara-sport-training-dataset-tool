import sys
import os

import data_handling

from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QIcon

from gui.ApplicationWindow import ApplicationWindow


def main(argv):
    application = QApplication(argv)

    application_window = ApplicationWindow()
    script_dir = os.path.dirname(os.path.realpath(__file__))
    application_window.setWindowIcon(QIcon(script_dir + os.path.sep + 'logo.jpg'))

    application.setActiveWindow(application_window)
    sys.exit(application.exec_())

if __name__ == '__main__':
    main(sys.argv)
