import sqlite3
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent.parent
DATABASE_PATH = BASE_DIR / "data" / "anime.db"


def get_connection():
    connection = sqlite3.connect(DATABASE_PATH)
    connection.row_factory = sqlite3.Row
    return connection


def create_tables():
    connection = get_connection()

    # Table des series
    connection.execute("""
        CREATE TABLE IF NOT EXISTS serie (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            titre TEXT NOT NULL,
            titre_original TEXT,
            image TEXT,
            description TEXT,
            annee INTEGER,
            genres TEXT,
            duree INTEGER,
            realisateur TEXT
        )
    """)

    connection.commit()
    connection.close()


def ajouter_serie(
    titre,
    titre_original,
    image,
    description,
    annee,
    genres,
    duree,
    realisateur,
):
    connection = get_connection()

    cursor = connection.execute(
        """
        INSERT INTO serie (
            titre,
            titre_original,
            image,
            description,
            annee,
            genres,
            duree,
            realisateur
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            titre,
            titre_original,
            image,
            description,
            annee,
            genres,
            duree,
            realisateur,
        )
    )

    serie_id = cursor.lastrowid

    connection.commit()
    connection.close()

    return serie_id


def lister_series():
    connection = get_connection()

    series = connection.execute("""
        SELECT
            serie.id,
            serie.titre,
            serie.titre_original,
            serie.image,
            serie.description,
            serie.annee,
            serie.genres,
            serie.duree,
            serie.realisateur
        FROM serie
        ORDER BY serie.titre COLLATE NOCASE ASC, serie.annee ASC
    """).fetchall()

    connection.close()

    return [
        {
            "id": serie["id"],
            "titre": serie["titre"],
            "titre_original": serie["titre_original"],
            "image": serie["image"],
            "description": serie["description"],
            "annee": serie["annee"],
            "genres": serie["genres"],
            "duree": serie["duree"],
            "realisateur": serie["realisateur"],
        }
        for serie in series
    ]



def supprimer_serie(serie_id):
    connection = get_connection()


    connection.execute(
        """
        DELETE FROM serie
        WHERE id = ?
        """,
        (
            serie_id,
        )
    )

    connection.commit()
    connection.close()


def recuperer_serie(serie_id):
    connection = get_connection()

    serie = connection.execute(
        """
        SELECT
            serie.id,
            serie.titre,
            serie.titre_original,
            serie.image,
            serie.description,
            serie.annee,
            serie.genres,
            serie.duree,
            serie.realisateur
        FROM serie
        WHERE serie.id = ?
        """,
        (
            serie_id,
        )
    ).fetchone()

    connection.close()

    if serie is None:
        return None

    return {
        "id": serie["id"],
        "titre": serie["titre"],
        "titre_original": serie["titre_original"],
        "image": serie["image"],
        "description": serie["description"],
        "annee": serie["annee"],
        "genres": serie["genres"],
        "duree": serie["duree"],
        "realisateur": serie["realisateur"],
    }