from PyQt5.QtWidgets import QStackedWidget
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QAction

from hexoskin.qt5_gui.sync_feeds.SyncFeedsInterface import SyncFeedsInterface
from hexoskin.qt5_gui.export_data.ExportDataInterface import ExportDataInterface
from hexoskin.qt5_gui.SharedData import SharedData


class ApplicationWindow(QMainWindow):
    def __init__(self, parent=None):
        super(ApplicationWindow, self).__init__(parent)
        self.shared_data = SharedData()

        self.title = 'Hexoskin Analysis Tool'
        self.left = 0
        self.top = 0
        self.width = 1600
        self.height = 1200
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.statusBar()
        self.create_layout()
        self.create_menu()
        self.show()

    def create_layout(self):
        self.setCentralWidget(SyncFeedsInterface(self, self.shared_data))

    def create_menu(self):
        # Create the actions
        show_sync_feeds = QAction('Synchronize and Tag feeds', self)
        show_sync_feeds.setStatusTip("Show the synchronisation and tag management interface")
        show_sync_feeds.triggered.connect(self.show_sync_feed_interface)

        show_export_data = QAction('Export data', self)
        show_export_data.setStatusTip("Show the data exportation interface")
        show_export_data.triggered.connect(self.show_export_data_interface)

        menu_bar = self.menuBar()

        window_menu = menu_bar.addMenu('Window')
        window_menu.addAction(show_sync_feeds)
        window_menu.addAction(show_export_data)

    def show_sync_feed_interface(self):
        self.setCentralWidget(SyncFeedsInterface(self, self.shared_data))

    def show_export_data_interface(self):
        self.setCentralWidget(ExportDataInterface(self, self.shared_data))