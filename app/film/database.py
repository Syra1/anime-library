from app.common.database import (get_connection, execute_query, fetch_all, fetch_one)

def create_tables():
    connection = get_connection()

    # Table des films
    connection.execute("""
        CREATE TABLE IF NOT EXISTS film (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            titre TEXT NOT NULL,
            titre_original TEXT,
            image TEXT,
            description TEXT,
            annee INTEGER,
            genres TEXT,
            duree INTEGER,
            realisateur TEXT,
            collection_id INTEGER,
            collection_nom TEXT
        )
    """)

    connection.commit()
    connection.close()

def ajouter_film(titre, titre_original, image, description, annee, genres, duree, realisateur, collection_id, collection_nom,):
    cursor = execute_query(
        """
        INSERT INTO film (titre, titre_original, image, description, annee, genres, duree, realisateur, collection_id, collection_nom)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (titre, titre_original, image, description, annee, genres, duree, realisateur, collection_id, collection_nom,)
    )

    return cursor.lastrowid

def lister_films():
    films = fetch_all(
        """
        SELECT
            film.id,
            film.titre,
            film.titre_original,
            film.image,
            film.description,
            film.annee,
            film.genres,
            film.duree,
            film.realisateur,
            film.collection_id,
            film.collection_nom
        FROM film
        ORDER BY COALESCE(film.collection_nom, film.titre) COLLATE NOCASE ASC, film.annee ASC, film.titre COLLATE NOCASE ASC
        """
    )

    return [
        {
            "id": film["id"],
            "titre": film["titre"],
            "titre_original": film["titre_original"],
            "image": film["image"],
            "description": film["description"],
            "annee": film["annee"],
            "genres": film["genres"],
            "duree": film["duree"],
            "realisateur": film["realisateur"],
            "collection_id": film["collection_id"],
            "collection_nom": film["collection_nom"],
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
            film.titre,
            film.titre_original,
            film.image,
            film.description,
            film.annee,
            film.genres,
            film.duree,
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
        "titre": film["titre"],
        "titre_original": film["titre_original"],
        "image": film["image"],
        "description": film["description"],
        "annee": film["annee"],
        "genres": film["genres"],
        "duree": film["duree"],
        "realisateur": film["realisateur"],
        "collection_id": film["collection_id"],
        "collection_nom": film["collection_nom"],
    }