import os
import shutil

from PySide2.QtCore import Slot
from PySide2.QtWidgets import QGridLayout, QPushButton, QFileDialog, QApplication, QMainWindow, QAction, QWidget

from ElimineDoublons import ElimineWindow, WidgetDoublons
from constants import CONF_DIR, PATH_NON_EPUB, PATH_NON_TRAITES, PATH_TRAITES, PATH_DEJA_EXISTANTS, PATH_DOSSIER, \
    PATH_DOUBLONS
from importer import Importer

# INITIALISATION
os.makedirs(CONF_DIR, exist_ok=True)
os.makedirs(PATH_TRAITES, exist_ok=True)
os.makedirs(PATH_NON_EPUB, exist_ok=True)
os.makedirs(PATH_NON_TRAITES, exist_ok=True)
os.makedirs(PATH_DEJA_EXISTANTS, exist_ok=True)
os.makedirs(PATH_DOUBLONS, exist_ok=True)


def reset():
    files = os.listdir(PATH_DEJA_EXISTANTS)
    NEW_PATH = os.path.join(PATH_DOSSIER, "Collection Que Sais-je")
    for file in files:
        shutil.move(f"{PATH_DEJA_EXISTANTS}/{file}", NEW_PATH)


class MainWidget(QWidget):
    def __init__(self):
        QWidget.__init__(self)

        self.setup_ui()
        self.setup_connections()

    # noinspection PyAttributeOutsideInit
    def setup_ui(self):
        self.btn_file_select = QPushButton('Sélectionner (fichiers)...')
        self.btn_dir_select = QPushButton('Sélectionner (répertoire)...')
        self.btn_execute = QPushButton('Exécuter...')
        self.btn_reset = QPushButton('Reset...')
        self.btn_elimine_doublons = QPushButton('Eliminer les doublons')

        # QWidget Layout
        self.layout = QGridLayout()
        self.layout.addWidget(self.btn_file_select, 0, 0)
        self.layout.addWidget(self.btn_dir_select, 0, 1)
        self.layout.addWidget(self.btn_execute, 0, 2)
        self.layout.addWidget(self.btn_reset, 0, 3)
        # self.layout.addWidget(self.btn_elimine_doublons, 0, 4)

        self.setLayout(self.layout)

    def setup_connections(self):
        self.btn_execute.clicked.connect(Importer)
        self.btn_reset.clicked.connect(reset)
        self.btn_file_select.clicked.connect(self.selection_livres)
        self.btn_dir_select.clicked.connect(self.selection_rep)
        # self.btn_elimine_doublons.clicked.connect(self.elimine_doublons)

    def selection_livres(self):
        selection = QFileDialog.getOpenFileNames(self, self.tr("Sélectionner un ou des fichier(s)"),
                                                 "/media/frederic/data",
                                                 self.tr(
                                                     "Ebook Files (*.epub *.moby *.pdf);; Archives Files (*.zip *.rar)"))[
            0]
        return

    def selection_rep(self):
        selection = QFileDialog.getExistingDirectory(self, self.tr("Sélectionner le répertoire"),
                                                     "/media/frederic/data", QFileDialog.ShowDirsOnly)
        importage = Importer(selection)
        importage.liste_fichiers()
        print(type(selection))
        return


class MainWindow(QMainWindow):
    def __init__(self, widget):
        super().__init__()
        self.win_elimine = None
        self.setWindowTitle('Import Ebook')

        # Menu
        self.menu = self.menuBar()
        self.file_menu = self.menu.addMenu("Fichier")
        self.tools_menu = self.menu.addMenu("Outils")

        # Exit QAction
        exit_action = QAction("Quitter", self)
        exit_action.setShortcut("Ctrl+Q")
        exit_action.triggered.connect(self.exit_app)
        self.file_menu.addAction(exit_action)

        # Tools
        suppress_double_action = QAction("Supprimer doublons", self)
        suppress_double_action.triggered.connect(self.elimine_doublons)
        self.tools_menu.addAction(suppress_double_action)

        self.setCentralWidget(widget)

    @Slot()
    def exit_app(self, checked):
        QApplication.quit()

    @Slot()
    def elimine_doublons(self, checked):
        if self.win_elimine is None:
            self.main_widget = WidgetDoublons()
            self.win_elimine = ElimineWindow(self.main_widget)
            self.win_elimine.show()

        else:
            self.win_elimine.close()
            self.win_elimine = None


if __name__ == "__main__":
    app = QApplication([])
    main_widget = MainWidget()
    win = MainWindow(main_widget)
    win.show()
    app.exec_()
