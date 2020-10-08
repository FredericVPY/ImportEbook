from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class ImportTemp(Base):
    __tablename__ = 'import_temp'
    """Classe du modèle d'un enregistrement d'import

    Args:
        db ([type]): [description]

    Returns:
        [type]: [description]
    """

    id = Column(Integer, primary_key=True)
    titre = Column(String(200),
                   nullable=True)
    auteur = Column(String(100),
                    nullable=True)
    isbn = Column(String(50),
                  unique=True,
                  nullable=True)
    ebook_code = Column(String(100),
                        unique=True,
                        nullable=True)


class ImportLivre(Base):
    """Classe du modèle d'un enregistrement d'import

    Args:
        db ([type]): [description]

    Returns:
        [type]: [description]
    """

    __tablename__ = 'import'
    id = Column(Integer,
                primary_key=True)
    titre = Column(String(50),
                   unique=False, nullable=True)
    auteur = Column(String(100),
                    unique=False,
                    nullable=True)
    isbn = Column(String(50),
                  unique=True,
                  nullable=True)
    ebook_code = Column(String(100),
                        unique=True,
                        nullable=True)
    path = Column(String(300),
                  unique=True,
                  nullable=False)
    identifiable = Column(Boolean,
                          unique=False,
                          nullable=False)
    doublon = Column(Boolean,
                     unique=False,
                     nullable=False)
    taille = Column(Integer,
                    unique=True,
                    nullable=True)
    hash = Column(String(50),
                  unique=True,
                  nullable=False)
    date_import = Column(DateTime,
                         unique=False,
                         nullable=False)
    date_traitement = Column(DateTime,
                             unique=False,
                             nullable=False)
    traite = Column(Boolean,
                    unique=False,
                    nullable=False)

    def __repr__(self):
        return '<User %r>' % self.username
