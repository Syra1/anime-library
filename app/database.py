import sqlite3

DATABASE_PATH = "data/anime.db"


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
            statut TEXT
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


def ajouter_anime(titre, titre_original, statut):
    connection = get_connection()

    cursor = connection.execute(
        """
        INSERT INTO anime (titre, titre_original, statut)
        VALUES (?, ?, ?)
        """,
        (titre, titre_original, statut)
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


def marquer_saison_vue(anime_id, saison_id):
    connection = get_connection()

    connection.execute(
        """
        INSERT INTO saison_vue (anime_id, saison_id)
        VALUES (?, ?)
        """,
        (anime_id, saison_id)
    )

    connection.commit()
    connection.close()


def lister_animes():
    connection = get_connection()

    cursor = connection.execute("""
        SELECT id, titre, titre_original, statut
        FROM anime
    """)

    animes = cursor.fetchall()

    connection.close()

    return animes

def get_saison(anime_id, numero):
    connection = get_connection()

    cursor = connection.execute(
        """
        SELECT id
        FROM saison
        WHERE anime_id = ? AND numero = ?
        """,
        (anime_id, numero)
    )

    saison = cursor.fetchone()

    connection.close()

    return saison

def lister_animes_avec_saisons():
    connection = get_connection()

    animes = connection.execute("""
        SELECT id, titre, titre_original, statut
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
            "statut": anime["statut"],
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
    statut,
    episodes
):

    anime_id = ajouter_anime(
        titre,
        titre_original,
        statut
    )


    if episodes:

        for numero in range(1, episodes + 1):

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
