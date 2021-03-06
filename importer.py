'''
Classe importer.py comporte tous les éléments pour importer un livre en base de données
'''

import os
import shutil
from glob import glob

from ebooklib import epub
from sqlalchemy import create_engine
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import sessionmaker

import constants
import models

dbstring = "postgres+psycopg2://adm_archiv:Dixf+483@172.18.0.2:5432/ArchivEbook"
db = create_engine(dbstring)
models.Base.metadata.bind = db
DBSession = sessionmaker(bind=db)

session = DBSession()


class Importer:
    def __init__(self, path):
        self.path = path

    def liste_fichiers(self):
        if os.path.isdir(self.path):
            liste_livre = glob(os.path.join(self.path, "**"), recursive=True)  # créer liste de fichiers dans le dossier
        else:
            liste_livre = self.path

        # Tri des fichiers epub / non epub
        liste_livres_autre_format = []  # liste des non epubs
        liste_livres_epub = []  # liste des epubs
        liste_livre_deja_existants = []
        # nbr_livre = len(liste_livre)
        # print(liste_livre)

        for livre in liste_livre:
            if livre.endswith(".epub"):
                liste_livres_epub.append(livre)
            else:
                if os.path.isfile(livre):
                    try:
                        liste_livres_autre_format.append(livre)
                        shutil.move(livre, constants.PATH_NON_EPUB)
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
                # print(book.get_metadata('DC','language'), book.get_metadata('DC','format'),
                # book.get_metadata('DC','date'))
                # print(book.get_metadata('DC','rights'), book.get_metadata('DC','coverage'),
                # book.get_metadata('DC','type'))

                # Ajout en base de données
                if isbn[0][0].startswith('978') or isbn[0][0].startswith('979'):
                    newimport = models.ImportTemp(auteur=auteur[0][0], titre=titre[0][0], isbn=isbn[0][0])
                    # print(auteur[0][0], titre[0][0])
                else:
                    newimport = models.ImportTemp(auteur=auteur[0][0], titre=titre[0][0], ebook_code=isbn[0][0])
                try:
                    session.add(newimport)
                    session.commit()
                except IntegrityError as e:
                    print(f"L'entrée existe déjà")
                    # except InvalidRequestError as e:
                    session.rollback()
                    liste_livre_deja_existants.append(ebook)
                    # print(f"L'entrée {e} existe déjà")
                    try:
                        shutil.move(ebook, constants.PATH_DEJA_EXISTANTS)
                    except:
                        pass
                finally:
                    session.close()
        # print(session.query(models.ImportTemp.titre).all())
        # print(liste_livres_erreur)
        # print(liste_livres_autre_format)


if __name__ == "__main__":
    print("OK")
