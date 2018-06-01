import sys
import os
from PyQt5.Qt import QApplication
from PyQt5.QtGui import QIcon
from hexoskin.qt5_gui import ApplicationWindow


def main():
    app = QApplication(sys.argv)
    scriptDir = os.path.dirname(os.path.realpath(__file__))
    appwindow = ApplicationWindow()
    appwindow.setWindowIcon(QIcon(scriptDir + os.path.sep + 'logo-hexoskin.jpg'))
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
