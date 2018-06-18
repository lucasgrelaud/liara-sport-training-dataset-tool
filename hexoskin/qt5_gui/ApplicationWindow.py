from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QAction

from hexoskin.qt5_gui.sync_feeds.SyncFeeds import SyncFeedsWidget
from hexoskin.qt5_gui.SharedData import SharedData


class ApplicationWindow(QMainWindow):
    def __init__(self, parent=None):
        super(ApplicationWindow, self).__init__(parent)
        self.shared_data = SharedData()

        self.sync_feeds_widget = None

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
        self.create_menu()
        self.create_layout()
        self.show()

    def create_layout(self):
        self.sync_feeds_widget = SyncFeedsWidget(self, self.shared_data)
        self.setCentralWidget(self.sync_feeds_widget)

    def create_menu(self):
        # Create the actions
        show_sync_feeds = QAction("Sync Feeds", self)
        show_sync_feeds.setStatusTip("Show the synchronisation and tag management window")
        show_sync_feeds.triggered.connect(self.show_sync_feed_window)

        window_menu = self.menuBar().addMenu("&Window")
        window_menu.addAction(show_sync_feeds)

    def show_sync_feed_window(self):
        self.setCentralWidget(self.sync_feeds_widget)
        self.show()
