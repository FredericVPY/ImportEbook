""" Classe importer.py comporte tous les éléments pour importer un livre en base de données
"""

import os
import shutil
from glob import glob

from ebooklib import epub
from sqlalchemy import create_engine
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.exc import UnmappedInstanceError

import constants
import models

dbstring = "postgres+psycopg2://adm_archiv:Dixf+483@172.18.0.2:5432/ArchivEbook"
db = create_engine(dbstring)
models.Base.metadata.bind = db
DBSession = sessionmaker(bind=db)

session = DBSession()


def check_epub(path):
    """
    Fonction qui retourne True si c'est un epub, False si non epub
    :param path: Chemin complet du livre à insérer
    :return: True ou False
    """
    if os.path.isfile(path):
        ebook = os.path.realpath(path)
        if ebook.endswith(".epub"):
            return True
        else:
            shutil.move(ebook, constants.PATH_NON_EPUB)
        return False
    else:
        return False


def files_list(path):
    """
    Fonction qui retourne une liste de fichiers à partir d'un path
    :param path: Chemin complet du livre à insérer
    :return: epub_list
    """
    epub_list = []
    liste_livre = glob(os.path.join(path, "**"), recursive=True)  # créer liste de fichiers dans le dossier
    for ebook in liste_livre:
        is_epub = check_epub(ebook)  # test si epub
        if is_epub:
            epub_list.append(ebook)
        else:
            liste_livres_autre_format = []  # liste des non epubs
    return epub_list


class EbookImport:
    epub_list_dict = []

    def __init__(self, path):
        self.path = path
        self.titre = ''
        self.auteur = ''
        self.isbn = ''

    def read_metadata(self, path):
        """
        Fonction qui lit les metadatas (auteur, titre, isbn) d'un ebook
        :param path: Chemin complet du livre à insérer
        :return: none
        """
        epub_dict = {}
        try:
            book = epub.read_epub(path)
        except AttributeError:
            print('erreur')
        else:
            self.titre = book.get_metadata('DC', 'title')
            self.auteur = book.get_metadata('DC', 'creator')
            self.isbn = book.get_metadata('DC', 'identifier')
            # print(book.get_metadata('DC','language'), book.get_metadata('DC','format'),
            # book.get_metadata('DC','date'))
            # print(book.get_metadata('DC','rights'), book.get_metadata('DC','coverage'),
            # book.get_metadata('DC','type'))
            epub_dict['titre'] = self.titre[0][0]
            epub_dict['auteur'] = self.auteur[0][0]
            epub_dict['isbn'] = self.isbn[0][0]
            self.epub_list_dict.append(epub_dict)

    def ebook_insert(self, path):
        """
        Insertion d'un ebook en base de données
        :param path: Chemin complet du livre à insérer
        :return: none
        """
        new_import = ''
        if self.isbn[0][0].startswith('978') or self.isbn[0][0].startswith('979'):
            try:
                new_import = models.ImportTemp(auteur=self.auteur[0][0], titre=self.titre[0][0], isbn=self.isbn[0][0])
            except IndexError as e:
                print(f'{e}')
        else:
            try:
                new_import = models.ImportTemp(auteur=self.auteur[0][0], titre=self.titre[0][0],
                                               ebook_code=self.isbn[0][0])
            except IndexError as e:
                print(f'{e}')

        try:
            session.add(new_import)
            session.commit()
        except UnmappedInstanceError as e:
            shutil.move(path, constants.PATH_NON_TRAITES)
            print(f'{e}')
        except IntegrityError as e:
            print(f"L'entrée existe déjà")
            # except InvalidRequestError as e:
            session.rollback()
            # liste_livre_deja_existants.append(ebook)
            # print(f"L'entrée {e} existe déjà")
            shutil.move(path, constants.PATH_DEJA_EXISTANTS)
        finally:
            session.close()


class FolderImport(EbookImport):
    def __init__(self, path, epub_list):
        super().__init__(path)
        self.epub_list = epub_list

    def ebook_bulk_insert(self, epub_list):
        """
        Fonction qui fait un insert multiple d'objets EbookImport
        :param epub_list:
        :return:
        """
        for ebook in epub_list:
            ebook_to_insert = EbookImport(ebook)
            ebook_to_insert.read_metadata(ebook)

        session.bulk_insert_mappings(models.ImportTemp, self.epub_list_dict)


if __name__ == "__main__":
    print("OK")
