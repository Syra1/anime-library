import sqlite3
from pathlib import Path
from app.config import DATABASE_PATH

# Ouvre une connexion à la base de données.
def get_connection():
    connection = sqlite3.connect(DATABASE_PATH)
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA foreign_keys = ON")
    return connection

# Exécute une requête qui modifie la base de données.
def execute_query(requete, parametres=()):
    connection = get_connection()
    cursor = connection.execute(requete, parametres)
    connection.commit()
    connection.close()
    return cursor

# Récupère plusieurs résultats d'une requête.
def fetch_all(requete, parametres=()):
    connection = get_connection()
    resultats = connection.execute(requete, parametres).fetchall()
    connection.close()
    return resultats

# Récupère un résultat d'une requête.
def fetch_one(requete, parametres=()):
    connection = get_connection()
    resultat = connection.execute(requete, parametres).fetchone()
    connection.close()
    return resultat

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
        "total": (resultats["films"] + resultats["animes"] + resultats["series"])
    }

def modifier_saison_vue(nom_media, saison_id, vu):
    execute_query(
        f"""
        UPDATE saison_{nom_media}
        SET vu = ?
        WHERE id = ?
        """,
        (vu, saison_id)
    )