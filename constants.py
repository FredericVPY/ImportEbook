import os

CUR_DIR = os.path.dirname(os.path.abspath(__file__))
CONF_DIR = os.path.join(CUR_DIR, 'Config')
CONF_FILE = os.path.join(CONF_DIR, 'config.json')
DEFAULT_PATH_DOSSIER = '/media/frederic/data/Livres/python_MB/'
PATH_DOSSIER = DEFAULT_PATH_DOSSIER
PATH_DEST = '/media/frederic/data/Livres/ImportEbook'
PATH_TRAITES = os.path.join(PATH_DEST, 'Traites')
PATH_NON_EPUB = os.path.join(PATH_DEST, 'Non_Epub')
PATH_NON_TRAITES = os.path.join(PATH_DEST, 'Non_Traites')
PATH_DEJA_EXISTANTS = os.path.join(PATH_DEST, 'Deja_Existants')
