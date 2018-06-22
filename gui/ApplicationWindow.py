from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QAction

from gui import SharedData
from gui.synchronization import SynchronizationInterface


class ApplicationWindow(QMainWindow):
    def __init__(self, parent=None):
        super(ApplicationWindow, self).__init__(parent)
        self.shared_data = SharedData()

        self.title = 'Training Dataset Creation Tool'
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
        self.setCentralWidget(SynchronizationInterface(self, self.shared_data))

    def create_menu(self):
        # TODO: Edit the menus
        # Create the actions
        show_sync_feeds = QAction('Synchronize feeds', self)
        show_sync_feeds.setStatusTip("Show the synchronisation interface")
        show_sync_feeds.triggered.connect(self.show_sync_feed_interface)

        show_tag_data = QAction('Tag data', self)
        show_tag_data.setStatusTip("Show the data tagging interface")
        show_tag_data.triggered.connect(self.show_tag_data_interface)

        show_export_data = QAction('Export data', self)
        show_export_data.setStatusTip("Show the data exportation interface")
        show_export_data.triggered.connect(self.show_export_data_interface)

        menu_bar = self.menuBar()

        window_menu = menu_bar.addMenu('Window')
        window_menu.addAction(show_sync_feeds)
        window_menu.addAction(show_tag_data)

    def show_sync_feed_interface(self):
        pass

    def show_tag_data_interface(self):
        pass

    def show_export_data_interface(self):
        pass