import sqlite3

from app.config import BASE_DIR


DATABASE_PATH = BASE_DIR / "data" / "anime.db"


def get_connection():
    connection = sqlite3.connect(DATABASE_PATH)
    connection.row_factory = sqlite3.Row
    return connection


def compter_contenus():

    connection = get_connection()

    resultats = connection.execute("""
        SELECT
            (SELECT COUNT(*) FROM film) AS films,
            (SELECT COUNT(*) FROM anime) AS animes
    """).fetchone()

    connection.close()

    return {
        "films": resultats["films"],
        "animes": resultats["animes"],
        "total": (
            resultats["films"]
            + resultats["animes"]
        )
    }