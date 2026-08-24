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

    # Table des films
    connection.execute("""
        CREATE TABLE IF NOT EXISTS film (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            titre TEXT NOT NULL,
            titre_original TEXT,
            image TEXT,
            description TEXT,
            annee INTEGER,
            genres TEXT,
            duree INTEGER,
            realisateur TEXT,
            collection_id INTEGER,
            collection_nom TEXT
        )
    """)

    connection.commit()
    connection.close()


def ajouter_film(
    titre,
    titre_original,
    image,
    description,
    annee,
    genres,
    duree,
    realisateur,
    collection_id,
    collection_nom,
):
    connection = get_connection()

    cursor = connection.execute(
        """
        INSERT INTO film (
            titre,
            titre_original,
            image,
            description,
            annee,
            genres,
            duree,
            realisateur,
            collection_id,
            collection_nom
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
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
            collection_id,
            collection_nom,
        )
    )

    film_id = cursor.lastrowid

    connection.commit()
    connection.close()

    return film_id


def lister_films():
    connection = get_connection()

    films = connection.execute("""
        SELECT
            film.id,
            film.titre,
            film.titre_original,
            film.image,
            film.description,
            film.annee,
            film.genres,
            film.duree,
            film.realisateur,
            film.collection_id,
            film.collection_nom
        FROM film
        ORDER BY COALESCE(film.collection_nom, film.titre) COLLATE NOCASE ASC, film.annee ASC, film.titre COLLATE NOCASE ASC
    """).fetchall()

    connection.close()

    return [
        {
            "id": film["id"],
            "titre": film["titre"],
            "titre_original": film["titre_original"],
            "image": film["image"],
            "description": film["description"],
            "annee": film["annee"],
            "genres": film["genres"],
            "duree": film["duree"],
            "realisateur": film["realisateur"],
            "collection_id": film["collection_id"],
            "collection_nom": film["collection_nom"],
        }
        for film in films
    ]



def supprimer_film(film_id):
    connection = get_connection()


    connection.execute(
        """
        DELETE FROM film
        WHERE id = ?
        """,
        (
            film_id,
        )
    )

    connection.commit()
    connection.close()


def recuperer_film(film_id):
    connection = get_connection()

    film = connection.execute(
        """
        SELECT
            film.id,
            film.titre,
            film.titre_original,
            film.image,
            film.description,
            film.annee,
            film.genres,
            film.duree,
            film.realisateur,
            film.collection_id,
            film.collection_nom
        FROM film
        WHERE film.id = ?
        """,
        (
            film_id,
        )
    ).fetchone()

    connection.close()

    if film is None:
        return None

    return {
        "id": film["id"],
        "titre": film["titre"],
        "titre_original": film["titre_original"],
        "image": film["image"],
        "description": film["description"],
        "annee": film["annee"],
        "genres": film["genres"],
        "duree": film["duree"],
        "realisateur": film["realisateur"],
        "collection_id": film["collection_id"],
        "collection_nom": film["collection_nom"],
    }