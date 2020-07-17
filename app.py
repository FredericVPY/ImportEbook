import os
import shutil

from PySide2 import QtWidgets

from constants import CONF_DIR, PATH_NON_EPUB, PATH_NON_TRAITES, PATH_TRAITES, PATH_DEJA_EXISTANTS, PATH_DOSSIER
from importer import Importer

# INITIALISATION
os.makedirs(CONF_DIR, exist_ok=True)
os.makedirs(PATH_TRAITES, exist_ok=True)
os.makedirs(PATH_NON_EPUB, exist_ok=True)
os.makedirs(PATH_NON_TRAITES, exist_ok=True)
os.makedirs(PATH_DEJA_EXISTANTS, exist_ok=True)


def reset():
    files = os.listdir(PATH_DEJA_EXISTANTS)
    NEW_PATH = os.path.join(PATH_DOSSIER, "Collection Que Sais-je")
    for file in files:
        shutil.move(f"{PATH_DEJA_EXISTANTS}/{file}", NEW_PATH)


class App(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Import Ebook')
        # w = h = 1000
        # self.resize(w, h)
        self.setup_ui()
        self.setup_connections()

    def setup_ui(self):
        self.layout = QtWidgets.QGridLayout(self)
        self.btn_file_select = QtWidgets.QPushButton('Sélectionner (fichiers)...')
        self.btn_dir_select = QtWidgets.QPushButton('Sélectionner (répertoire)...')
        self.btn_execute = QtWidgets.QPushButton('Exécuter...')
        self.btn_reset = QtWidgets.QPushButton('Reset...')
        # prg_bar = QtWidgets.QProgressBar()
        self.layout.addWidget(self.btn_file_select, 0, 0)
        self.layout.addWidget(self.btn_dir_select, 0, 1)
        self.layout.addWidget(self.btn_execute, 0, 2)
        self.layout.addWidget(self.btn_reset, 0, 3)

    def setup_connections(self):
        self.btn_execute.clicked.connect(Importer)
        self.btn_reset.clicked.connect(reset)
        self.btn_file_select.clicked.connect(self.selection_livres)
        self.btn_dir_select.clicked.connect(self.selection_rep)

    def selection_livres(self):
        selection = QtWidgets.QFileDialog.getOpenFileNames(self,
                                                           self.tr("Ouvrir"), "/media/frederic/data",
                                                           self.tr(
                                                               "Ebook Files (*.epub *.moby *.pdf);; Archives Files (*.zip *.rar)"))[
            0]
        print(selection)
        print(type(selection))
        return

    def selection_rep(self):
        selection = QtWidgets.QFileDialog.getExistingDirectory(self, self.tr("Sélectionner le répertoire"),
                                                               "/media/frederic/data",
                                                               QtWidgets.QFileDialog.ShowDirsOnly)
        print(selection)
        print(type(selection))
        return


app = QtWidgets.QApplication([])
win = App()
win.show()
app.exec_()
