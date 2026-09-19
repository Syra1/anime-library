import json
import urllib.parse
import urllib.request

from app.config import TMDB_ACCESS_TOKEN
from app.config import (TMDB_API_URL, TMDB_HEADERS, TMDB_TIMEOUT, MAX_SEARCH_RESULTS, IMAGE_BASE_URL)
from app.common.gestion_erreur import gerer_erreur

from app.common.utils import (
    convertir_liste_en_texte,
    determiner_type_media,
    formater_duree,
)

def preparer_parametres(parametres):
    return urllib.parse.urlencode(parametres)


def creer_requete_tmdb(url):
    return urllib.request.Request(
        url,
        headers=TMDB_HEADERS,
        method="GET"
    )


def executer_requete_tmdb(requete):
    with urllib.request.urlopen(
        requete,
        timeout=TMDB_TIMEOUT
    ) as response:
        return json.loads(response.read())


def recuperer_aggregate_credits(media_id):
    url = (
        f"{TMDB_API_URL}/tv/"
        f"{media_id}/aggregate_credits"
    )

    requete = creer_requete_tmdb(url)

    try:
        return executer_requete_tmdb(requete)

    except Exception as erreur:
        return gerer_erreur(
            erreur,
            "récupération des crédits agrégés TMDB",
            {}
        )


def rechercher_medias(
    recherche,
    endpoint,
    titre,
    titre_original,
    date,
    type_media=None
):
    parametres = preparer_parametres({
        "query": recherche,
        "language": "fr-FR",
        "include_adult": "false",
        "page": 1
    })

    url = f"{TMDB_API_URL}/{endpoint}?{parametres}"

    requete = creer_requete_tmdb(url)

    try:
        resultat = executer_requete_tmdb(requete)

        medias = resultat.get("results", [])

        if type_media:
            medias = [
                media
                for media in medias
                if determiner_type_media(media) == type_media
            ]

        return [
            {
                "id": media["id"],
                "title": media.get(titre),
                "original_title": media.get(titre_original),
                "image": (
                    f"{IMAGE_BASE_URL}{media['poster_path']}"
                    if media.get("poster_path")
                    else None
                ),
                "annee": (
                    media[date][:4]
                    if media.get(date)
                    else None
                )
            }
            for media in medias[:MAX_SEARCH_RESULTS]
        ]

    except Exception as erreur:
        return gerer_erreur(
            erreur,
            "recherche TMDB",
            []
        )


def recuperer_media(
    media_id,
    endpoint,
    titre,
    titre_original,
    date
):
    parametres = preparer_parametres({
        "language": "fr-FR",
        "append_to_response": "credits,images",
        "include_image_language": "fr,en,null"
    })

    url = (
        f"{TMDB_API_URL}/{endpoint}/"
        f"{media_id}?{parametres}"
    )

    requete = creer_requete_tmdb(url)

    try:
        media = executer_requete_tmdb(requete)

        if not media:
            return None

        aggregate_credits = None

        if endpoint == "tv":
            aggregate_credits = recuperer_aggregate_credits(
                media_id
            )

        auteurs = ""

        if aggregate_credits:
            auteurs = convertir_liste_en_texte(
                personne["name"]
                for personne in aggregate_credits.get(
                    "crew",
                    []
                )
                if any(
                    job.get("job") in [
                        "Comic Book",
                        "Author"
                    ]
                    for job in personne.get("jobs", [])
                )
            )

        genres = convertir_liste_en_texte(
            genre["name"]
            for genre in media.get("genres", [])
        )

        realisateur = None

        if endpoint == "tv":
            realisateur = convertir_liste_en_texte(
                createur["name"]
                for createur in media.get("created_by", [])
            )

        else:
            for personne in media.get(
                "credits",
                {}
            ).get("crew", []):

                if personne.get("job") == "Director":
                    realisateur = personne.get("name")
                    break

        saisons = []

        if endpoint == "tv":
            saisons = [
                {
                    "numero": saison["season_number"],
                    "titre": saison["name"],
                    "nombre_episodes": saison["episode_count"]
                }
                for saison in media.get("seasons", [])
                if saison["season_number"] != 0
            ]

        collection = media.get(
            "belongs_to_collection"
        )

        collection_id = (
            collection.get("id")
            if collection
            else None
        )

        collection_nom = (
            collection.get("name")
            if collection
            else None
        )

        posters = media.get(
            "images",
            {}
        ).get(
            "posters",
            []
        )

        image_secondaire = None

        for poster in posters:
            if poster["file_path"] != media.get(
                "poster_path"
            ):
                image_secondaire = (
                    f"{IMAGE_BASE_URL}"
                    f"{poster['file_path']}"
                )
                break

        return {
            "id": media["id"],
            "titre": media.get(titre),
            "titre_original": media.get(titre_original),
            "image": (
                f"{IMAGE_BASE_URL}{media['poster_path']}"
                if media.get("poster_path")
                else None
            ),
            "image_secondaire": image_secondaire,
            "description": media.get("overview") or "",
            "annee": (
                int(media[date][:4])
                if media.get(date)
                else None
            ),
            "genres": genres,
            "duree": formater_duree(
                media.get("runtime")
                or (
                    media["episode_run_time"][0]
                    if media.get("episode_run_time")
                    else None
                )
            ),
            "auteur": auteurs,
            "realisateur": realisateur,
            "media": media,
            "aggregate_credits": aggregate_credits,
            "nombre_saisons": (
                media.get("number_of_seasons")
                if endpoint == "tv"
                else None
            ),
            "saisons": saisons,
            "collection_id": collection_id,
            "collection_nom": collection_nom,
        }

    except Exception as erreur:
        return gerer_erreur(
            erreur,
            "récupération du média TMDB",
            None
        )


def recuperer_collection(collection_id):
    parametres = preparer_parametres({
        "language": "fr-FR"
    })

    url = (
        f"{TMDB_API_URL}/collection/"
        f"{collection_id}?{parametres}"
    )

    requete = creer_requete_tmdb(url)

    try:
        collection = executer_requete_tmdb(requete)

        if not collection:
            return None

        return collection.get("parts", [])

    except Exception as erreur:
        return gerer_erreur(
            erreur,
            "récupération de la collection TMDB",
            None
        )