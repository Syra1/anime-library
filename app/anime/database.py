from app.common.database import (get_connection, execute_query, fetch_all, fetch_one, modifier_saison_vue, creer_suivi_media)

def modifier_saison_vue_anime(saisons_ids, vu):
    modifier_saison_vue("anime", saisons_ids, vu)

def create_tables():
    connection = get_connection()
    connection.execute(
    """
        CREATE TABLE IF NOT EXISTS anime (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            tmdb_id INTEGER NOT NULL,
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
        CREATE TABLE IF NOT EXISTS saison_anime (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            anime_id INTEGER NOT NULL,
            titre TEXT,
            numero INTEGER NOT NULL,
            nombre_episodes INTEGER NOT NULL,
            vu INTEGER NOT NULL DEFAULT 0,
            FOREIGN KEY (anime_id) REFERENCES anime(id) ON DELETE CASCADE
        )
    """)

    connection.commit()
    connection.close()

def ajouter_anime(tmdb_id, titre, titre_original, image, description, annee, genres, duree, auteur, realisateur, nombre_saisons, saisons):
    cursor = execute_query(
        """
        INSERT INTO anime (tmdb_id, titre, titre_original, image, description, annee, genres, duree, auteur, realisateur, nombre_saisons)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (tmdb_id, titre, titre_original, image, description, annee, genres, duree, auteur, realisateur, nombre_saisons,)
    )

    anime_id = cursor.lastrowid

    for saison in saisons:
        execute_query(
            """
            INSERT INTO saison_anime (
                anime_id,
                titre,
                numero,
                nombre_episodes
            )
            VALUES (?, ?, ?, ?)
            """,
            (anime_id, saison["titre"], saison["numero"], saison["nombre_episodes"],)
        )

    return anime_id

def lister_animes():
    animes = fetch_all(
        """
        SELECT
            anime.id,
            anime.tmdb_id,
            anime.titre,
            anime.titre_original,
            anime.image,
            anime.description,
            anime.annee,
            anime.genres,
            anime.auteur,
            anime.duree,
            anime.realisateur,
            anime.nombre_saisons
        FROM anime
        ORDER BY anime.titre COLLATE NOCASE ASC, anime.annee ASC
        """
    )

    return [
        {
            "id": anime["id"],
            "tmdb_id": anime["tmdb_id"],
            "titre": anime["titre"],
            "titre_original": anime["titre_original"],
            "image": anime["image"],
            "description": anime["description"],
            "annee": anime["annee"],
            "genres": anime["genres"],
            "duree": anime["duree"],
            "auteur": anime["auteur"],
            "realisateur": anime["realisateur"],
            "nombre_saisons": anime["nombre_saisons"],
            "suivi": creer_suivi_media(compter_saisons_vues(anime["id"]), anime["nombre_saisons"]),
        }
        for anime in animes
    ]

def supprimer_anime(anime_id):
    execute_query("""
        DELETE FROM anime
        WHERE id = ?
    """, (anime_id,))

def recuperer_anime(anime_id):
    anime = fetch_one(
        """
        SELECT
            anime.id,
            anime.tmdb_id,
            anime.titre,
            anime.titre_original,
            anime.image,
            anime.description,
            anime.annee,
            anime.genres,
            anime.duree,
            anime.auteur,
            anime.realisateur,
            anime.nombre_saisons
        FROM anime
        WHERE anime.id = ?
        """,
        (anime_id,)
    )

    if anime is None:
        return None

    saisons = fetch_all(
        """
        SELECT
            id,
            titre,
            numero,
            nombre_episodes,
            vu
        FROM saison_anime
        WHERE anime_id = ?
        ORDER BY numero ASC
        """,
        (anime_id,)
    )

    return {
        "id": anime["id"],
        "tmdb_id": anime["tmdb_id"],
        "titre": anime["titre"],
        "titre_original": anime["titre_original"],
        "image": anime["image"],
        "description": anime["description"],
        "annee": anime["annee"],
        "genres": anime["genres"],
        "duree": anime["duree"],
        "auteur": anime["auteur"],
        "realisateur": anime["realisateur"],
        "nombre_saisons": anime["nombre_saisons"],
        "saisons": [
            {
                "id": saison["id"],
                "titre": saison["titre"],
                "numero": saison["numero"],
                "nombre_episodes": saison["nombre_episodes"],
                "vu": saison["vu"],
            }
            for saison in saisons
        ],
    }

def compter_saisons_vues(anime_id):
    saisons = fetch_all(
        """
        SELECT vu
        FROM saison_anime
        WHERE anime_id = ?
        """,
        (anime_id,)
    )

    return sum(
        saison["vu"]
        for saison in saisons
    )