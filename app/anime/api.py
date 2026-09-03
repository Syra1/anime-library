import json

import urllib.request
import urllib.error
import urllib.parse

from app.config import TMDB_ACCESS_TOKEN


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


# Exécute la requête pour l'API TMDB.

def executer_requete_tmdb(requete):

    with urllib.request.urlopen(
        requete,
        timeout=TMDB_TIMEOUT
    ) as response:

        resultat = json.loads(
            response.read()
        )

    return resultat


# Convertit une liste en texte.

def convertir_liste_en_texte(elements):

    return ", ".join(
        element
        for element in elements
        if element
    )


# Determiner si anime ou serie

def determiner_type_media(media):

    genres = media.get(
        "genres",
        []
    )

    genre_ids = [
        genre.get("id")
        for genre in genres
    ]

    if 16 not in genre_ids:
        return "serie"

    return "anime"


# Recherche une série dans la base de données TMDB.

def rechercher_animes(recherche):

    parametres = preparer_parametres({
        "query": recherche,
        "language": "fr-FR",
        "include_adult": "false",
        "page": 1
    })

    url = (
        f"{TMDB_API_URL}/search/tv?"
        f"{parametres}"
    )

    requete = creer_requete_tmdb(url)

    try:

        resultat = executer_requete_tmdb(
            requete
        )

        animes = resultat.get(
            "results",
            []
        )

        animes_filtrees = []

        for anime in animes:

            details = recuperer_anime(
                anime["id"]
            )

            if details is None:
                continue

            if details["type"] != "anime":
                continue

            animes_filtrees.append(
                anime
            )

        animes = animes_filtrees

        recherche_lower = recherche.lower()


        def score_anime(anime):

            titres = [
                anime.get("name"),
                anime.get("original_name")
            ]

            titres = [
                titre.lower()
                for titre in titres
                if titre
            ]

            meilleur_score = NO_SCORE

            for titre in titres:

                if titre == recherche_lower:

                    score = 0

                elif titre.startswith(
                    recherche_lower
                ):

                    score = 10

                elif recherche_lower in titre:

                    score = 100

                else:

                    score = NO_SCORE

                meilleur_score = min(
                    meilleur_score,
                    score
                )

            return meilleur_score


        animes = sorted(
            animes,
            key=score_anime
        )


        return [

            {
                "id": anime["id"],

                "title": anime.get(
                    "name"
                ),

                "original_title": anime.get(
                    "original_name"
                ),

                "image": (
                    f"{IMAGE_BASE_URL}"
                    f"{anime['poster_path']}"
                    if anime.get("poster_path")
                    else None
                ),

                "annee": (
                    anime["first_air_date"][:4]
                    if anime.get("first_air_date")
                    else None
                )
            }

            for anime in animes[
                :MAX_SEARCH_RESULTS
            ]

        ]


    except urllib.error.HTTPError as error:

        print(
            f"Erreur HTTP TMDB : {error.code}"
        )

        print(
            error.read().decode("utf-8")
        )

        return []


    except urllib.error.URLError as error:

        print(
            "Erreur de connexion à TMDB :"
        )

        print(error.reason)

        return []


    except TimeoutError:

        print(
            "TMDB a mis trop de temps à répondre."
        )

        return []


    except Exception as erreur:

        print(
            "Erreur recherche TMDB :",
            erreur
        )

        return []


# Récupère une série depuis TMDB.

def recuperer_anime(anime_id):
    parametres = preparer_parametres({
        "language": "fr-FR",
        "append_to_response": "credits"
    })
    url = (f"{TMDB_API_URL}/tv/" f"{anime_id}?{parametres}")
    requete = creer_requete_tmdb(url)
    try:
        media = executer_requete_tmdb(requete)
        if not media:
            return None
        type_media = determiner_type_media(media)
        titre = (media.get("name") or media.get("original_name"))
        titre_original = (media.get("original_name") or media.get("name"))
        image = (
            f"{IMAGE_BASE_URL}"
            f"{media['poster_path']}"
            if media.get("poster_path")
            else None)
        description = (media.get("overview") or "")
        annee = None
        if media.get("first_air_date"):
            annee = int(media["first_air_date"][:4])
        genres = convertir_liste_en_texte([genre["name"]
            for genre in media.get("genres", [])])
        duree = None
        durees_episodes = media.get(
            "episode_run_time", [])
        if durees_episodes:
            duree = durees_episodes[0]
        realisateur = None
        createurs = media.get("created_by", [])
        if createurs:
            realisateur = createurs[0].get("name")
        nombre_saisons = media.get("number_of_seasons", 0)
        saisons = []
        for saison in media.get("seasons", []):
            numero = saison.get("season_number")
            if numero == 0:
                continue
            saisons.append({
                "numero": numero,
                "nombre_episodes": saison.get("episode_count", 0),
            })

        return {
            "titre": titre,
            "titre_original": titre_original,
            "image": image,
            "description": description,
            "annee": annee,
            "genres": genres,
            "duree": duree,
            "realisateur": realisateur,
            "nombre_saisons": nombre_saisons,
            "saisons": saisons,
            "type": type_media,

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