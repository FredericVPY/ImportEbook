import os
import shutil
from glob import glob

from ebooklib import epub
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import models

dbstring = "postgres://adm_archiv:Dixf+483@localhost/ArchivEbook"

db = create_engine(dbstring)
models.Base.metadata.bind = db
DBSession = sessionmaker(bind=db)

session = DBSession()

# INITIALISATION
CUR_FILE = __file__
CUR_DIR = os.path.dirname(CUR_FILE)
CONF_DIR = os.path.join(CUR_DIR, 'Config')
CONF_FILE = os.path.join(CONF_DIR, 'config.json')
os.makedirs(CONF_DIR, exist_ok=True)

DEFAULT_PATH_DOSSIER = '/media/frederic/data/Livres/python_MB/'
PATH_DOSSIER = DEFAULT_PATH_DOSSIER

PATH_TRAITES = os.path.join(PATH_DOSSIER, 'Traites')
PATH_NON_EPUB = os.path.join(PATH_DOSSIER, 'Non_Epub')
PATH_NON_TRAITES = os.path.join(PATH_DOSSIER, 'Non_Traites')
PATH_DEJA_EXISTANTS = os.path.join(PATH_DOSSIER, 'Deja_Existants')
os.makedirs(PATH_TRAITES, exist_ok=True)
os.makedirs(PATH_NON_EPUB, exist_ok=True)
os.makedirs(PATH_NON_TRAITES, exist_ok=True)
os.makedirs(PATH_DEJA_EXISTANTS, exist_ok=True)

liste_livre = glob(os.path.join(PATH_DOSSIER, "**"), recursive=True)

# Tri des fichiers epub / non epub
liste_livres_autre_format = []  # liste des non epubs
liste_livres_epub = []  # liste des epubs
liste_livre_deja_existants = []
for livre in liste_livre:
    if livre.endswith(".epub"):
        liste_livres_epub.append(livre)
    else:
        if os.path.isfile(livre):
            try:
                liste_livres_autre_format.append(livre)
                shutil.move(livre, PATH_NON_EPUB)
            except:
                print("erreur")

# Traitement des epubs
liste_livres_erreur = []
for ebook in liste_livres_epub:
    try:
        book = epub.read_epub(ebook)
    except AttributeError:
        liste_livres_erreur.append(ebook)
    else:
        titre = book.get_metadata('DC', 'title')
        auteur = book.get_metadata('DC', 'creator')
        isbn = book.get_metadata('DC', 'identifier')
        # print(book.get_metadata('DC','language'), book.get_metadata('DC','format'),book.get_metadata('DC','date'))
        # print(book.get_metadata('DC','rights'), book.get_metadata('DC','coverage'),book.get_metadata('DC','type'))

        # Ajout en base de données
        if isbn[0][0].startswith('978') or isbn[0][0].startswith('979'):
            newimport = models.ImportTemp(auteur=auteur[0][0], titre=titre[0][0], isbn=isbn[0][0])
        else:
            newimport = models.ImportTemp(auteur=auteur[0][0], titre=titre[0][0], ebook_code=isbn[0][0])

        try:
            session.add(newimport)
            session.commit()
        except:
            liste_livre_deja_existants.append(ebook)
            try:
                shutil.move(ebook, PATH_DEJA_EXISTANTS)
            except:
                pass
# print(session.query(models.Import_temp.titre).all())
print(liste_livres_erreur)
print(liste_livres_autre_format)
