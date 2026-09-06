import json
import urllib.request
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