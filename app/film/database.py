from app.common.database import (get_connection, execute_query, fetch_all, fetch_one, creer_suivi_media)

def create_tables():
    connection = get_connection()

    # Table des films
    connection.execute("""
        CREATE TABLE IF NOT EXISTS film (
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
            collection_id INTEGER,
            collection_nom TEXT
        )
    """)

    connection.commit()
    connection.close()

def ajouter_film(tmdb_id, titre, titre_original, image, description, annee, genres, duree, auteur, realisateur, collection_id, collection_nom,):
    cursor = execute_query(
        """
        INSERT INTO film (tmdb_id, titre, titre_original, image, description, annee, genres, duree, auteur, realisateur, collection_id, collection_nom)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (tmdb_id, titre, titre_original, image, description, annee, genres, duree, auteur, realisateur, collection_id, collection_nom,)
    )

    return cursor.lastrowid

def creer_suivis_collections(films):
    from app.common.media import recuperer_collection
    suivis = {}
    collections_deja_traitees = []
    for film in films:
        collection_id = film["collection_id"]
        if collection_id is None:
            continue
        if collection_id in collections_deja_traitees:
            continue

        collections_deja_traitees.append(collection_id)

        films_tmdb = recuperer_collection(collection_id)

        if films_tmdb is None:
            continue

        films_locaux = [
            film_local
            for film_local in films
            if film_local["collection_id"] == collection_id
        ]

        suivis[collection_id] = creer_suivi_media(
            len(films_locaux),
            len(films_tmdb)
        )

    return suivis

def lister_films():
    films = fetch_all(
        """
        SELECT
            film.id,
            film.tmdb_id,
            film.titre,
            film.titre_original,
            film.image,
            film.description,
            film.annee,
            film.genres,
            film.duree,
            film.auteur,
            film.realisateur,
            film.collection_id,
            film.collection_nom
        FROM film
        ORDER BY COALESCE(film.collection_nom, film.titre) COLLATE NOCASE ASC, film.annee ASC, film.titre COLLATE NOCASE ASC
        """
    )

    suivis = creer_suivis_collections(films)

    return [
        {
            "id": film["id"],
            "tmdb_id": film["tmdb_id"],
            "titre": film["titre"],
            "titre_original": film["titre_original"],
            "image": film["image"],
            "description": film["description"],
            "annee": film["annee"],
            "genres": film["genres"],
            "duree": film["duree"],
            "auteur": film["auteur"],
            "realisateur": film["realisateur"],
            "collection_id": film["collection_id"],
            "collection_nom": film["collection_nom"],
            "suivi": suivis.get(film["collection_id"]),
        }
        for film in films
    ]

def supprimer_film(film_id):
    execute_query("""
        DELETE FROM film
        WHERE id = ?
    """, (film_id,))

def recuperer_film(film_id):
    film = fetch_one(
        """
        SELECT
            film.id,
            film.tmdb_id,
            film.titre,
            film.titre_original,
            film.image,
            film.description,
            film.annee,
            film.genres,
            film.duree,
            film.auteur,
            film.realisateur,
            film.collection_id,
            film.collection_nom
        FROM film
        WHERE film.id = ?
        """,
        (film_id,)
    )

    if film is None:
        return None

    return {
        "id": film["id"],
        "tmdb_id": film["tmdb_id"],
        "titre": film["titre"],
        "titre_original": film["titre_original"],
        "image": film["image"],
        "description": film["description"],
        "annee": film["annee"],
        "genres": film["genres"],
        "duree": film["duree"],
        "auteur": film["auteur"],
        "realisateur": film["realisateur"],
        "collection_id": film["collection_id"],
        "collection_nom": film["collection_nom"],
    }