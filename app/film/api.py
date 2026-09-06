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