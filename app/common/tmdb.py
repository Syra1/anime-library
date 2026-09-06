import urllib.error
import json
import urllib.request
import urllib.parse

from app.config import TMDB_ACCESS_TOKEN
from app.common.media import (
    convertir_liste_en_texte,
    determiner_type_media,
)

TMDB_API_URL = "https://api.themoviedb.org/3"

TMDB_HEADERS = {
    "Authorization": f"Bearer {TMDB_ACCESS_TOKEN}",
    "Accept": "application/json"
}

TMDB_TIMEOUT = 10
MAX_SEARCH_RESULTS = 20
NO_SCORE = 999
IMAGE_BASE_URL = "https://image.tmdb.org/t/p/w500"


# Prépare les paramètres pour l'API TMDB.
def preparer_parametres(parametres):
    return urllib.parse.urlencode(
        parametres
    )


# Crée une requête pour l'API TMDB.
def creer_requete_tmdb(url):
    requete = urllib.request.Request(
        url,
        headers=TMDB_HEADERS,
        method="GET"
    )

    return requete


# Exécute une requête pour l'API TMDB.
def executer_requete_tmdb(requete):
    with urllib.request.urlopen(
        requete,
        timeout=TMDB_TIMEOUT
    ) as response:

        resultat = json.loads(
            response.read()
        )

    return resultat

def rechercher_medias(
    recherche,
    endpoint,
    titre,
    titre_original,
    date
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

    except urllib.error.HTTPError as error:
        print(f"Erreur HTTP TMDB : {error.code}")
        print(error.read().decode("utf-8"))
        return []

    except urllib.error.URLError as error:
        print("Erreur de connexion à TMDB :")
        print(error.reason)
        return []

    except TimeoutError:
        print("TMDB a mis trop de temps à répondre.")
        return []

    except Exception as erreur:
        print("Erreur recherche TMDB :", erreur)
        return []

def recuperer_media(
    media_id,
    endpoint,
    titre,
    titre_original,
    date
):
    parametres = preparer_parametres({
        "language": "fr-FR",
        "append_to_response": "credits"
    })

    url = f"{TMDB_API_URL}/{endpoint}/{media_id}?{parametres}"
    requete = creer_requete_tmdb(url)

    try:
        media = executer_requete_tmdb(requete)

        if not media:
            return None

        genres = convertir_liste_en_texte(
            genre["name"]
            for genre in media.get("genres", [])
        )

        realisateur = None

        for personne in media.get("credits", {}).get("crew", []):
            if personne.get("job") == "Director":
                realisateur = personne.get("name")
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
            "description": media.get("overview") or "",
            "annee": (
                int(media[date][:4])
                if media.get(date)
                else None
            ),
            "genres": genres,
            "duree": media.get("runtime"),
            "realisateur": realisateur,
            "media": media
        }

    except urllib.error.HTTPError as error:
        print(f"Erreur HTTP TMDB : {error.code}")
        print(error.read().decode("utf-8"))
        return None

    except urllib.error.URLError as error:
        print("Erreur de connexion à TMDB :")
        print(error.reason)
        return None

    except TimeoutError:
        print("TMDB a mis trop de temps à répondre.")
        return None

    except Exception as erreur:
        print("Erreur récupération TMDB :", erreur)
        return None