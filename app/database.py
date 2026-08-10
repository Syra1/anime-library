import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DATABASE_PATH = BASE_DIR / "data" / "anime.db"

def get_connection():
    connection = sqlite3.connect(DATABASE_PATH)
    connection.row_factory = sqlite3.Row
    return connection


def create_tables():
    connection = get_connection()

    # Table des animés
    connection.execute("""
        CREATE TABLE IF NOT EXISTS anime (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            titre TEXT NOT NULL,
            titre_original TEXT,
            image TEXT,
            description TEXT,
            nombre_episodes INTEGER
        )
    """)

    # Table des saisons
    connection.execute("""
        CREATE TABLE IF NOT EXISTS saison (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            anime_id INTEGER NOT NULL,
            numero INTEGER NOT NULL,
            FOREIGN KEY (anime_id) REFERENCES anime(id),
            UNIQUE (anime_id, numero)
        )
    """)

    # Table des saisons regardées
    connection.execute("""
        CREATE TABLE IF NOT EXISTS saison_vue (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            anime_id INTEGER NOT NULL,
            saison_id INTEGER NOT NULL,
            FOREIGN KEY (anime_id) REFERENCES anime(id),
            FOREIGN KEY (saison_id) REFERENCES saison(id),
            UNIQUE (anime_id, saison_id)
        )
    """)

    connection.commit()
    connection.close()


def ajouter_anime(titre, titre_original, image, description, nombre_episodes):
    connection = get_connection()

    cursor = connection.execute(
        """
        INSERT INTO anime (titre, titre_original, image, description, nombre_episodes)
        VALUES (?, ?, ?, ?, ?)
        """,
        (titre, titre_original, image, description, nombre_episodes)
    )

    anime_id = cursor.lastrowid

    connection.commit()
    connection.close()

    return anime_id


def ajouter_saison(anime_id, numero):
    connection = get_connection()

    cursor = connection.execute(
        """
        INSERT INTO saison (anime_id, numero)
        VALUES (?, ?)
        """,
        (anime_id, numero)
    )

    saison_id = cursor.lastrowid

    connection.commit()
    connection.close()

    return saison_id


def lister_animes_avec_saisons():
    connection = get_connection()

    animes = connection.execute("""
        SELECT id, titre, titre_original, image, description, nombre_episodes
        FROM anime
        ORDER BY titre
    """).fetchall()

    resultats = []

    for anime in animes:

        saisons = connection.execute("""
            SELECT
                saison.id,
                saison.numero,
                CASE
                    WHEN saison_vue.id IS NOT NULL THEN 1
                    ELSE 0
                END AS vue
            FROM saison
            LEFT JOIN saison_vue
                ON saison.id = saison_vue.saison_id
            WHERE saison.anime_id = ?
            ORDER BY saison.numero
        """, (anime["id"],)).fetchall()

        resultats.append({
            "id": anime["id"],
            "titre": anime["titre"],
            "titre_original": anime["titre_original"],
            "image": anime["image"],
            "description": anime["description"],
            "nombre_episodes": anime["nombre_episodes"],
            "saisons": [
                {
                    "id": saison["id"],
                    "numero": saison["numero"],
                    "vue": bool(saison["vue"])
                }
                for saison in saisons
            ]
        })

    connection.close()

    return resultats

def ajouter_anime_complet(
    titre,
    titre_original,
    image,
    nombre_saisons,
    description,
    nombre_episodes
):

    anime_id = ajouter_anime(
        titre,
        titre_original,
        image,
        description,
        nombre_episodes
    )

    for numero in range(1, nombre_saisons + 1):

        ajouter_saison(
            anime_id,
            numero
        )


    return anime_id

def modifier_saisons_vue(anime_id, saisons):

    connection = get_connection()

    for saison in saisons:

        if saison["vue"]:

            connection.execute(
                """
                INSERT OR IGNORE INTO saison_vue
                (anime_id, saison_id)
                VALUES (?, ?)
                """,
                (anime_id, saison["id"])
            )

        else:

            connection.execute(
                """
                DELETE FROM saison_vue
                WHERE anime_id = ?
                AND saison_id = ?
                """,
                (anime_id, saison["id"])
            )

    connection.commit()
    connection.close()

def supprimer_anime(anime_id):

    connection = get_connection()

    connection.execute(
        """
        DELETE FROM saison_vue
        WHERE anime_id = ?
        """,
        (anime_id,)
    )

    connection.execute(
        """
        DELETE FROM saison
        WHERE anime_id = ?
        """,
        (anime_id,)
    )

    connection.execute(
        """
        DELETE FROM anime
        WHERE id = ?
        """,
        (anime_id,)
    )

    connection.commit()
    connection.close()

def recuperer_anime_avec_saisons(anime_id):

    connection = get_connection()


    anime = connection.execute(
        """
        SELECT id, titre, titre_original, image, description, nombre_episodes
        FROM anime
        WHERE id = ?
        """,
        (anime_id,)
    ).fetchone()


    if anime is None:

        connection.close()
        return None


    saisons = connection.execute(
        """
        SELECT
            saison.id,
            saison.numero,
            CASE
                WHEN saison_vue.id IS NOT NULL THEN 1
                ELSE 0
            END AS vue

        FROM saison

        LEFT JOIN saison_vue
            ON saison.id = saison_vue.saison_id

        WHERE saison.anime_id = ?

        ORDER BY saison.numero
        """,
        (anime_id,)
    ).fetchall()


    connection.close()


    return {
        "id": anime["id"],
        "titre": anime["titre"],
        "titre_original": anime["titre_original"],
        "image": anime["image"],
        "description": anime["description"],
        "nombre_episodes": anime["nombre_episodes"],
        "saisons": [
            {
                "id": saison["id"],
                "numero": saison["numero"],
                "vue": bool(saison["vue"])
            }
            for saison in saisons
        ]
    }


def ajouter_saison_suivante(anime_id):
    connection = get_connection()

    derniere_saison = connection.execute(
        """
        SELECT MAX(numero) AS numero
        FROM saison
        WHERE anime_id = ?
        """,
        (anime_id,)
    ).fetchone()

    if derniere_saison["numero"] is None:
        numero = 1
    else:
        numero = derniere_saison["numero"] + 1

    cursor = connection.execute(
        """
        INSERT INTO saison (
            anime_id,
            numero,
            anilist_id,
            nombre_episodes
        )
        VALUES (?, ?, ?, ?)
        """,
        (
            anime_id,
            numero,
            None,
            None
        )
    )

    saison_id = cursor.lastrowid

    connection.commit()
    connection.close()

    return {
        "id": saison_id,
        "numero": numero,
        "nombre_episodes": None,
        "vue": False
    }

def supprimer_derniere_saison(anime_id):

    connection = get_connection()

    derniere = connection.execute(
        """
        SELECT id
        FROM saison
        WHERE anime_id = ?
        ORDER BY numero DESC, id DESC
        LIMIT 1
        """,
        (anime_id,)
    ).fetchone()

    if derniere is None:
        connection.close()
        return False

    connection.execute(
        "DELETE FROM saison_vue WHERE saison_id = ?",
        (derniere["id"],)
    )

    connection.execute(
        "DELETE FROM saison WHERE id = ?",
        (derniere["id"],)
    )

    connection.commit()
    connection.close()

    return True