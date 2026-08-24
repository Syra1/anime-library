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

            duree INTEGER

        )
    """)

    # Table des films regardés
    connection.execute("""
        CREATE TABLE IF NOT EXISTS film_vue (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            film_id INTEGER NOT NULL,

            FOREIGN KEY (film_id) REFERENCES film(id),

            UNIQUE (film_id)

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
            duree
        )
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
        (
            titre,
            titre_original,
            image,
            description,
            annee,
            genres,
            duree,
        )
    )

    film_id = cursor.lastrowid

    connection.commit()

    connection.close()

    return film_id


def ajouter_film_complet(
    titre,
    titre_original,
    image,
    description,
    annee,
    genres,
    duree,
):

    film_id = ajouter_film(
        titre,
        titre_original,
        image,
        description,
        annee,
        genres,
        duree,
    )

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

            CASE
                WHEN film_vue.id IS NOT NULL THEN 1
                ELSE 0
            END AS vue

        FROM film

        LEFT JOIN film_vue
            ON film.id = film_vue.film_id

        ORDER BY film.titre COLLATE NOCASE, film.annee

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
            "vue": bool(film["vue"]),
        }
        for film in films
    ]


def modifier_film_vue(
    film_id,
    vue,
):

    connection = get_connection()

    if vue:

        connection.execute(
            """
            INSERT OR IGNORE INTO film_vue (
                film_id
            )
            VALUES (?)
            """,
            (
                film_id,
            )
        )

    else:

        connection.execute(
            """
            DELETE FROM film_vue

            WHERE film_id = ?
            """,
            (
                film_id,
            )
        )

    connection.commit()

    connection.close()


def supprimer_film(film_id):

    connection = get_connection()

    connection.execute(
        """
        DELETE FROM film_vue

        WHERE film_id = ?
        """,
        (
            film_id,
        )
    )

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

            CASE
                WHEN film_vue.id IS NOT NULL THEN 1
                ELSE 0
            END AS vue

        FROM film

        LEFT JOIN film_vue
            ON film.id = film_vue.film_id

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
        "vue": bool(film["vue"]),
    }