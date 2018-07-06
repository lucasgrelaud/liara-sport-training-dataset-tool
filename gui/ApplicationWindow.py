from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QAction

from gui import SharedData
from gui.synchronization import SynchronizationInterface
from gui.exportation import ExportationInterface


class ApplicationWindow(QMainWindow):
    def __init__(self, parent=None):
        super(ApplicationWindow, self).__init__(parent)
        self.shared_data = SharedData()

        self.title = 'Training Dataset Creation Tool'
        self.left = 10
        self.top = 10
        self.width = 1280
        self.height = 720
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.statusBar()
        self.create_layout()
        self.create_menu()
        self.show()

    def create_layout(self):
        self.setCentralWidget(SynchronizationInterface(self, self.shared_data))

    def create_menu(self):
        # Create the actions
        show_sync_tag_data = QAction('Synchronize and tag', self)
        show_sync_tag_data.setStatusTip("Show the interface dedicated to synchronize and tag the data")
        show_sync_tag_data.triggered.connect(self.show_sync_tag_interface)

        show_export_data = QAction('Export data', self)
        show_export_data.setStatusTip("Show the data exportation interface")
        show_export_data.triggered.connect(self.show_export_data_interface)

        menu_bar = self.menuBar()

        window_menu = menu_bar.addMenu('Window')
        window_menu.addAction(show_sync_tag_data)
        window_menu.addAction(show_export_data)

    def show_sync_tag_interface(self):
        self.setCentralWidget(SynchronizationInterface(self, self.shared_data))

    def show_export_data_interface(self):
        self.setCentralWidget(ExportationInterface(self, self.shared_data))
