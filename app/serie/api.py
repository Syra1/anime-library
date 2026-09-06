from app.common.media import (
    convertir_liste_en_texte,
    determiner_type_media,
)

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
    serie = recuperer_media(
        serie_id,
        "tv",
        "name",
        "original_name",
        "first_air_date"
    )

    if not serie:
        return None

    media = serie["media"]

    createurs = convertir_liste_en_texte(
        createur["name"]
        for createur in media.get("created_by", [])
    )

    saisons = [
        {
            "numero": saison["season_number"],
            "titre": saison["name"],
            "nombre_episodes": saison["episode_count"]
        }
        for saison in media.get("seasons", [])
        if saison["season_number"] != 0
    ]

    serie["realisateur"] = createurs
    serie["nombre_saisons"] = media.get("number_of_seasons")
    serie["saisons"] = saisons

    return serie