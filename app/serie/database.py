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
        CREATE TABLE IF NOT EXISTS serie (
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
        CREATE TABLE IF NOT EXISTS saison_serie (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            serie_id INTEGER NOT NULL,
            numero INTEGER NOT NULL,
            nombre_episodes INTEGER NOT NULL,
            FOREIGN KEY (serie_id) REFERENCES serie(id) ON DELETE CASCADE
        )
    """)

    connection.commit()
    connection.close()

def ajouter_serie(titre, titre_original, image, description, annee, genres, duree, realisateur, nombre_saisons, saisons):
    connection = get_connection()
    cursor = connection.execute(
        """
        INSERT INTO serie (titre, titre_original, image, description, annee, genres, duree, realisateur, nombre_saisons)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (titre, titre_original, image, description, annee, genres, duree, realisateur, nombre_saisons,)
    )
    serie_id = cursor.lastrowid

    for saison in saisons:
        connection.execute(
            """
            INSERT INTO saison_serie (serie_id, numero, nombre_episodes)
            VALUES (?, ?, ?)
            """, (serie_id, saison["numero"], saison["nombre_episodes"], ) )
    connection.commit()
    connection.close()
    return serie_id

def lister_series():
    connection = get_connection()
    series = connection.execute(
        """
        SELECT serie.id, serie.titre, serie.titre_original, serie.image, serie.description, serie.annee, serie.genres,serie.duree, serie.realisateur, serie.nombre_saisons
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
            "nombre_saisons": serie["nombre_saisons"],
        }
        for serie in series
    ]

def supprimer_serie(serie_id):
    connection = get_connection()
    connection.execute(
        """
        DELETE FROM serie
        WHERE id = ?
        """, (serie_id,)
    )
    connection.commit()
    connection.close()

def recuperer_serie(serie_id):
    connection = get_connection()
    serie = connection.execute(
        """
        SELECT serie.id, serie.titre, serie.titre_original, serie.image, serie.description, serie.annee, serie.genres, serie.duree, serie.realisateur, serie.nombre_saisons
        FROM serie
        WHERE serie.id = ?
        """, (serie_id,)
    ).fetchone()
    if serie is None:
        connection.close()
        return None
    saisons = connection.execute(
        """
        SELECT id, numero, nombre_episodes
        FROM saison_serie
        WHERE serie_id = ?
        ORDER BY numero ASC
        """, (serie_id,)
    ).fetchall()
    connection.close()

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
        "nombre_saisons": serie["nombre_saisons"],
        "saisons": [
            {
                "id": saison["id"],
                "numero": saison["numero"],
                "nombre_episodes": saison["nombre_episodes"],
            }
            for saison in saisons
        ],
    }