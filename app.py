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
        self.btn_ouvrir = QtWidgets.QPushButton('Sélectionner...')
        self.btn_reset = QtWidgets.QPushButton('Reset...')
        # prg_bar = QtWidgets.QProgressBar()
        self.layout.addWidget(self.btn_ouvrir, 0, 0)
        self.layout.addWidget(self.btn_reset, 0, 1)

    def setup_connections(self):
        self.btn_ouvrir.clicked.connect(Importer)
        self.btn_reset.clicked.connect(reset)


app = QtWidgets.QApplication([])
win = App()
win.show()
app.exec_()
