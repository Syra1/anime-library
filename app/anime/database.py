import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent
DATABASE_PATH = BASE_DIR / "data" / "anime.db"

def get_connection():
    connection = sqlite3.connect(DATABASE_PATH)
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA foreign_keys = ON")
    return connection

def create_tables():
    connection = get_connection()
    connection.execute(
    """
        CREATE TABLE IF NOT EXISTS anime (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            titre TEXT NOT NULL,
            titre_original TEXT,
            image TEXT,
            description TEXT,
            annee INTEGER,
            genres TEXT,
            duree INTEGER,
            realisateur TEXT,
            nombre_saisons INTEGER
        )
    """)

    connection.execute(
    """
        CREATE TABLE IF NOT EXISTS saison_anime (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            anime_id INTEGER NOT NULL,
            numero INTEGER NOT NULL,
            nombre_episodes INTEGER NOT NULL,
            FOREIGN KEY (anime_id) REFERENCES anime(id) ON DELETE CASCADE
        )
    """)

    connection.commit()
    connection.close()

def ajouter_anime(titre, titre_original, image, description, annee, genres, duree, realisateur, nombre_saisons, saisons):
    connection = get_connection()
    cursor = connection.execute(
        """
        INSERT INTO anime (titre, titre_original, image, description, annee, genres, duree, realisateur, nombre_saisons)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (titre, titre_original, image, description, annee, genres, duree, realisateur, nombre_saisons,)
    )
    anime_id = cursor.lastrowid

    for saison in saisons:
        connection.execute(
            """
            INSERT INTO saison_anime (anime_id, numero, nombre_episodes)
            VALUES (?, ?, ?)
            """, (anime_id, saison["numero"], saison["nombre_episodes"], ) )
    connection.commit()
    connection.close()
    return anime_id

def lister_animes():
    connection = get_connection()
    animes = connection.execute(
        """
        SELECT anime.id, anime.titre, anime.titre_original, anime.image, anime.description, anime.annee, anime.genres, anime.duree, anime.realisateur, anime.nombre_saisons
        FROM anime
        ORDER BY anime.titre COLLATE NOCASE ASC, anime.annee ASC
    """).fetchall()
    connection.close()
    return [
        {
            "id": anime["id"],
            "titre": anime["titre"],
            "titre_original": anime["titre_original"],
            "image": anime["image"],
            "description": anime["description"],
            "annee": anime["annee"],
            "genres": anime["genres"],
            "duree": anime["duree"],
            "realisateur": anime["realisateur"],
            "nombre_saisons": anime["nombre_saisons"],
        }
        for anime in animes
    ]

def supprimer_anime(anime_id):
    connection = get_connection()
    connection.execute(
        """
        DELETE FROM anime
        WHERE id = ?
        """, (anime_id,)
    )
    connection.commit()
    connection.close()

def recuperer_anime(anime_id):
    connection = get_connection()
    anime = connection.execute(
        """
        SELECT anime.id, anime.titre, anime.titre_original, anime.image, anime.description, anime.annee, anime.genres, anime.duree, anime.realisateur, anime.nombre_saisons
        FROM anime
        WHERE anime.id = ?
        """, (anime_id,)
    ).fetchone()
    if anime is None:
        connection.close()
        return None
    saisons = connection.execute(
        """
        SELECT id, numero, nombre_episodes
        FROM saison_anime
        WHERE anime_id = ?
        ORDER BY numero ASC
        """, (anime_id,)
    ).fetchall()
    connection.close()

    return {
        "id": anime["id"],
        "titre": anime["titre"],
        "titre_original": anime["titre_original"],
        "image": anime["image"],
        "description": anime["description"],
        "annee": anime["annee"],
        "genres": anime["genres"],
        "duree": anime["duree"],
        "realisateur": anime["realisateur"],
        "nombre_saisons": anime["nombre_saisons"],
        "saisons": [
            {
                "id": saison["id"],
                "numero": saison["numero"],
                "nombre_episodes": saison["nombre_episodes"],
            }
            for saison in saisons
        ],
    }