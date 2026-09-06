from app.common.media import (
    convertir_liste_en_texte,
    determiner_type_media,
)

from app.common.tmdb import (
    rechercher_medias,
    recuperer_media,
)


# Recherche un film dans la base de données TMDB.
def rechercher_films(recherche):
    return rechercher_medias(
        recherche,
        "search/movie",
        "title",
        "original_title",
        "release_date"
    )


# Récupère un film depuis TMDB.
def recuperer_film(film_id):
    film = recuperer_media(
        film_id,
        "movie",
        "title",
        "original_title",
        "release_date"
    )

    if not film:
        return None

    media = film["media"]

    collection = media.get("belongs_to_collection")

    film["collection_id"] = (
        collection.get("id")
        if collection
        else None
    )

    film["collection_nom"] = (
        collection.get("name")
        if collection
        else None
    )

    return film