from app.common.tmdb import (
    rechercher_medias,
    recuperer_media,
)


# Recherche un anime dans la base de données TMDB.
def rechercher_animes(recherche):
    return rechercher_medias(
        recherche,
        "search/tv",
        "name",
        "original_name",
        "first_air_date"
    )


# Récupère un anime depuis TMDB.
def recuperer_anime(anime_id):
    return recuperer_media(
        anime_id,
        "tv",
        "name",
        "original_name",
        "first_air_date"
    )