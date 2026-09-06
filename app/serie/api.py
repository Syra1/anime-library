from app.common.tmdb import (
    rechercher_medias,
    recuperer_media,
)


# Recherche une série dans la base de données TMDB.
def rechercher_series(recherche):
    return rechercher_medias(
        recherche,
        "search/tv",
        "name",
        "original_name",
        "first_air_date"
    )


# Récupère une série depuis TMDB.
def recuperer_serie(serie_id):
    return recuperer_media(
        serie_id,
        "tv",
        "name",
        "original_name",
        "first_air_date"
    )