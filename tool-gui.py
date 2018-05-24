import sys
from PyQt5.Qt import QApplication
from hexoskin.qt5_gui import ApplicationWindow


def main():
    app = QApplication(sys.argv)
    appwindow = ApplicationWindow()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
