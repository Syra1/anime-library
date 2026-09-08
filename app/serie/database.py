from app.common.database import (get_connection, execute_query, fetch_all, fetch_one)

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
            auteur TEXT,
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

def ajouter_serie(titre, titre_original, image, description, annee, genres, duree, auteur, realisateur, nombre_saisons, saisons):
    cursor = execute_query(
        """
        INSERT INTO serie (titre, titre_original, image, description, annee, genres, duree, auteur, realisateur, nombre_saisons)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (titre, titre_original, image, description, annee, genres, duree, auteur, realisateur, nombre_saisons,)
    )

    serie_id = cursor.lastrowid

    for saison in saisons:
        execute_query(
            """
            INSERT INTO saison_serie (
                serie_id,
                numero,
                nombre_episodes
            )
            VALUES (?, ?, ?)
            """,
            (
                serie_id,
                saison["numero"],
                saison["nombre_episodes"],
            )
        )

    return serie_id

def lister_series():
    series = fetch_all(
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
            serie.auteur,
            serie.realisateur,
            serie.nombre_saisons
        FROM serie
        ORDER BY serie.titre COLLATE NOCASE ASC, serie.annee ASC
        """
    )

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
            "auteur": serie["auteur"],
            "realisateur": serie["realisateur"],
            "nombre_saisons": serie["nombre_saisons"],
        }
        for serie in series
    ]

def supprimer_serie(serie_id):
    execute_query("""
        DELETE FROM serie
        WHERE id = ?
    """, (serie_id,))

def recuperer_serie(serie_id):
    serie = fetch_one(
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
            serie.realisateur,
            serie.nombre_saisons
        FROM serie
        WHERE serie.id = ?
        """,
        (serie_id,)
    )

    if serie is None:
        return None

    saisons = fetch_all(
        """
        SELECT
            id,
            numero,
            nombre_episodes
        FROM saison_serie
        WHERE serie_id = ?
        ORDER BY numero ASC
        """,
        (serie_id,)
    )

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