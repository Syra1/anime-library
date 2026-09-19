import sqlite3
from contextlib import contextmanager

from app.config import DATABASE_PATH


# Ouvre une connexion à la base de données et la ferme automatiquement
# à la sortie du bloc "with", même en cas d'erreur.
@contextmanager
def get_connection():
    connection = sqlite3.connect(DATABASE_PATH)
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA foreign_keys = ON")

    try:
        yield connection
    finally:
        connection.close()


# Exécute une requête qui modifie la base de données.
def execute_query(requete, parametres=()):
    with get_connection() as connection:
        cursor = connection.execute(requete, parametres)
        connection.commit()
        return cursor


# Récupère plusieurs résultats d'une requête.
def fetch_all(requete, parametres=()):
    with get_connection() as connection:
        return connection.execute(requete, parametres).fetchall()


# Récupère un résultat d'une requête.
def fetch_one(requete, parametres=()):
    with get_connection() as connection:
        return connection.execute(requete, parametres).fetchone()


def compter_contenus():
    resultats = fetch_one("""
        SELECT
            (SELECT COUNT(*) FROM film) AS films,
            (SELECT COUNT(*) FROM anime) AS animes,
            (SELECT COUNT(*) FROM serie) AS series
    """)

    return {
        "films": resultats["films"],
        "animes": resultats["animes"],
        "series": resultats["series"],
        "total": (resultats["films"] + resultats["animes"] + resultats["series"]),
    }


def modifier_saison_vue(nom_media, saisons_ids, vu):
    if not saisons_ids:
        return

    placeholders = ", ".join("?" for _ in saisons_ids)

    execute_query(
        f"""
        UPDATE saison_{nom_media}
        SET vu = ?
        WHERE id IN ({placeholders})
        """,
        (vu, *saisons_ids),
    )


# ----------------------------------------------------------------------
# Création des tables
# ----------------------------------------------------------------------
#
# Les tables "serie" et "anime" partagent exactement le même schéma
# (seul le nom de la table change), tout comme "saison_serie" et
# "saison_anime". On génère donc ces schémas à partir d'un gabarit
# commun plutôt que de les dupliquer.
#
# NB : ces noms de table/colonne doivent rester cohérents avec
# MEDIA_CONFIG dans media_manager.py.

def _schema_media_simple():
    return """
        CREATE TABLE IF NOT EXISTS film (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            tmdb_id INTEGER NOT NULL,
            titre TEXT NOT NULL,
            titre_original TEXT,
            image TEXT,
            image_secondaire TEXT,
            description TEXT,
            annee INTEGER,
            genres TEXT,
            duree TEXT,
            auteur TEXT,
            realisateur TEXT,
            collection_id INTEGER,
            collection_nom TEXT
        )
    """


def _schema_media_avec_saisons(table):
    return f"""
        CREATE TABLE IF NOT EXISTS {table} (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            tmdb_id INTEGER NOT NULL,
            titre TEXT NOT NULL,
            titre_original TEXT,
            image TEXT,
            image_secondaire TEXT,
            description TEXT,
            annee INTEGER,
            genres TEXT,
            duree TEXT,
            auteur TEXT,
            realisateur TEXT,
            nombre_saisons INTEGER
        )
    """


def _schema_saisons(table_saison, id_saison, table_parente):
    return f"""
        CREATE TABLE IF NOT EXISTS {table_saison} (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            {id_saison} INTEGER NOT NULL,
            titre TEXT,
            numero INTEGER NOT NULL,
            nombre_episodes INTEGER NOT NULL,
            vu INTEGER NOT NULL DEFAULT 0,
            FOREIGN KEY ({id_saison})
                REFERENCES {table_parente}(id)
                ON DELETE CASCADE
        )
    """


SCHEMAS = [
    _schema_media_simple(),
    _schema_media_avec_saisons("serie"),
    _schema_saisons("saison_serie", "serie_id", "serie"),
    _schema_media_avec_saisons("anime"),
    _schema_saisons("saison_anime", "anime_id", "anime"),
]


def create_tables():
    with get_connection() as connection:
        for schema in SCHEMAS:
            connection.execute(schema)

        connection.commit()