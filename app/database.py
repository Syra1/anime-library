import sqlite3

DATABASE_PATH = "data/anime.db"


def get_connection():
    connection = sqlite3.connect(DATABASE_PATH)
    return connection

def create_tables():
    connection = get_connection()

    connection.execute("""
        CREATE TABLE IF NOT EXISTS anime (
            id INTEGER PRIMARY KEY,
            titre TEXT NOT NULl,
            titre_original TEXT,
            vu INTEGER NOT NULL DEFAULT 0
        )
    """)

    connection.commit()
    connection.close()

def ajouter_anime(titre, titre_original, vu):
    connection = get_connection()

    connection.execute(
        """
        INSERT INTO anime (titre, titre_original, vu)
        VALUES (?, ?, ?)
        """,
        (titre, titre_original, vu)
    )

    connection.commit()
    connection.close()

def lister_animes():
    connection = get_connection()

    cursor = connection.execute("""
        SELECT id, titre, titre_original, vu
        FROM anime
    """)

    animes = cursor.fetchall()

    connection.close()

    return animes
