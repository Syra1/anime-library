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
IMAGE_BASE_URL = "https://image.tmdb.org/t/p/w500"

# Prépare les paramètres pour l'API TMDB.
def preparer_parametres(parametres):
    return urllib.parse.urlencode(parametres)

# Crée une requête pour l'API TMDB.
def creer_requete_tmdb(url):
    requete = urllib.request.Request(url, headers=TMDB_HEADERS, method="GET")
    return requete

# Exécute une requête pour l'API TMDB.
def executer_requete_tmdb(requete):
    with urllib.request.urlopen(requete, timeout=TMDB_TIMEOUT) as response:
        resultat = json.loads(response.read())
    return resultat

def recuperer_aggregate_credits(media_id):
    url = f"{TMDB_API_URL}/tv/{media_id}/aggregate_credits"
    requete = creer_requete_tmdb(url)
    try:
        return executer_requete_tmdb(requete)
    except urllib.error.HTTPError as error:
        print(f"Erreur HTTP TMDB : {error.code}")
        print(error.read().decode("utf-8"))
        return {}

    except urllib.error.URLError as error:
        print("Erreur de connexion à TMDB :")
        print(error.reason)
        return {}

    except TimeoutError:
        print("TMDB a mis trop de temps à répondre.")
        return {}

    except Exception as erreur:
        print("Erreur crédits agrégés TMDB :", erreur)
        return {}

def rechercher_medias(recherche, endpoint, titre, titre_original, date, type_media):
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
        medias = [media for media in resultat.get("results", []) if determiner_type_media(media) == type_media]

        return [
            {
                "id": media["id"],
                "title": media.get(titre),
                "original_title": media.get(titre_original),
                "image": (f"{IMAGE_BASE_URL}{media['poster_path']}" if media.get("poster_path") else None),
                "annee": (media[date][:4] if media.get(date) else None)
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

def recuperer_media(media_id, endpoint, titre, titre_original, date):
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

        aggregate_credits = None

        if endpoint == "tv":
            aggregate_credits = recuperer_aggregate_credits(media_id)

        auteurs = ""

        if aggregate_credits:
            auteurs = convertir_liste_en_texte(
                personne["name"]
                for personne in aggregate_credits.get("crew", [])
                if any(
                    job.get("job") in ["Comic Book", "Author"]
                    for job in personne.get("jobs", [])
                )
            )

        genres = convertir_liste_en_texte(genre["name"] for genre in media.get("genres", []))

        realisateur = None

        if endpoint == "tv":
            realisateur = convertir_liste_en_texte(createur["name"] for createur in media.get("created_by", []))
        else:
            for personne in media.get("credits", {}).get("crew", []):
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

        collection = media.get("belongs_to_collection")
        collection_id = (collection.get("id") if collection else None)
        collection_nom = (collection.get("name") if collection else None)

        resultat = {
            "id": media["id"],
            "titre": media.get(titre),
            "titre_original": media.get(titre_original),
            "image": (f"{IMAGE_BASE_URL}{media['poster_path']}" if media.get("poster_path") else None),
            "description": media.get("overview") or "",
            "annee": (int(media[date][:4]) if media.get(date) else None),
            "genres": genres,
            "duree": (media.get("runtime") or (media["episode_run_time"][0] if media.get("episode_run_time") else None)),
            "auteur": auteurs,
            "realisateur": realisateur,
            "media": media,
            "aggregate_credits": aggregate_credits,
            "nombre_saisons": (media.get("number_of_seasons") if endpoint == "tv" else None),
            "saisons": saisons,
            "collection_id": collection_id,
            "collection_nom": collection_nom,
        }
        return resultat

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
        print("Erreur récupération TMDB :", repr(erreur))
        return None