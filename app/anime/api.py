import urllib.error
from app.common.tmdb import (
    TMDB_API_URL,
    MAX_SEARCH_RESULTS,
    NO_SCORE,
    IMAGE_BASE_URL,
    preparer_parametres,
    creer_requete_tmdb,
    executer_requete_tmdb,
    rechercher_medias,
    recuperer_media,
)

from app.common.media import (
    convertir_liste_en_texte,
    determiner_type_media,
)

# Recherche une série dans la base de données TMDB.

def rechercher_animes(recherche):
    return rechercher_medias(
        recherche,
        "search/tv",
        "name",
        "original_name",
        "first_air_date"
    )


# Récupère une série depuis TMDB.

def recuperer_anime(anime_id):
    media = recuperer_media(
        anime_id,
        "tv"
    )

    if not media:
        return None

    type_media = determiner_type_media(media)

    titre = media.get("name")
    titre_original = media.get("original_name")

    image = (
        f"{IMAGE_BASE_URL}{media['poster_path']}"
        if media.get("poster_path")
        else None
    )

    description = media.get("overview")

    annee = (
        media["first_air_date"][:4]
        if media.get("first_air_date")
        else None
    )

    genres = convertir_liste_en_texte(
        genre["name"]
        for genre in media.get("genres", [])
    )

    duree_episode = (
        media["episode_run_time"][0]
        if media.get("episode_run_time")
        else None
    )

    createurs = convertir_liste_en_texte(
        createur["name"]
        for createur in media.get("created_by", [])
    )

    nombre_saisons = media.get("number_of_seasons")

    saisons = [
        {
            "numero": saison["season_number"],
            "titre": saison["name"],
            "nombre_episodes": saison["episode_count"]
        }
        for saison in media.get("seasons", [])
        if saison["season_number"] != 0
    ]

    return {
        "id": media["id"],
        "type": type_media,
        "titre": titre,
        "titre_original": titre_original,
        "image": image,
        "description": description,
        "annee": annee,
        "genres": genres,
        "duree": duree_episode,
        "realisateur": createurs,
        "nombre_saisons": nombre_saisons,
        "saisons": saisons
    }