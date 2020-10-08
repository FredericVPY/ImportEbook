from PySide2.QtCore import Slot
from PySide2.QtWidgets import QWidget, QVBoxLayout, QAction, QMainWindow, QTableWidget, QHeaderView


class WidgetDoublons(QWidget):
    def __init__(self):
        QWidget.__init__(self)

        self.setup_ui()
        self.setup_connections()

    # noinspection PyAttributeOutsideInit
    def setup_ui(self):
        # Left
        self.table = QTableWidget()
        self.table.setColumnCount(2)
        self.table.setHorizontalHeaderLabels(["Nom", "Chemin"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        #
        # # QWidget Layout
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.table)
        # self.layout.addWidget(self.btn_dir_select, 0, 1)
        # self.layout.addWidget(self.btn_execute, 0, 2)
        # self.layout.addWidget(self.btn_reset, 0, 3)
        # self.layout.addWidget(self.btn_elimine_doublons, 0, 4)

        self.setLayout(self.layout)

    def setup_connections(self):
        pass


class ElimineWindow(QMainWindow):
    def __init__(self, widget):
        super().__init__()
        self.setWindowTitle('Suppression des doublons')

        # Menu
        self.menu = self.menuBar()
        self.file_menu = self.menu.addMenu("Fichier")
        self.tools_menu = self.menu.addMenu("Outils")

        # Open QAction
        open_action = QAction("Sélectionner", self)
        open_action.triggered.connect(self.open_app)
        self.file_menu.addAction(open_action)

        # Close QAction
        close_action = QAction("Fermer", self)
        close_action.setShortcut("Ctrl+Q")
        close_action.triggered.connect(self.close_app)
        self.file_menu.addAction(close_action)

        # Tools
        suppress_double_action = QAction("Supprimer doublons", self)
        # suppress_double_action.triggered.connect(self.elimine_doublons)
        self.tools_menu.addAction(suppress_double_action)

        self.setCentralWidget(widget)

    @Slot()
    def open_app(self, checked):
        print('bonjour')

    @Slot()
    def close_app(self, checked):
        print('au revoir')
