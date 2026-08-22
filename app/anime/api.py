import json
import urllib.request
import urllib.error


ANILIST_API_URL = "https://graphql.anilist.co"
ANILIST_HEADERS = {
    "Content-Type": "application/json",
    "Accept": "application/json",
    "User-Agent": "anime-library/1.0"
}
ANILIST_TIMEOUT = 10
MAX_SEARCH_RESULTS = 10
NO_SCORE = 999

# Prépare les données pour la base de données.
def preparer_donnees(query, variables):
    donnees = json.dumps({
        "query": query,
        "variables": variables
    }).encode("utf-8")
    return donnees

# Crée une requete pour l'API AniList.
def creer_requete_anilist(donnees):
    requete = urllib.request.Request(
        ANILIST_API_URL,
        data=donnees,
        headers=ANILIST_HEADERS,
        method="POST"
    )
    return requete

# Execute la requete pour l'API AniList.
def executer_requete_anilist(requete):
    with urllib.request.urlopen(
        requete,
        timeout=ANILIST_TIMEOUT
    ) as response:
        resultat = json.loads(response.read())
    return resultat

# Recherche un anime dans la base de donnée.
def rechercher_animes(recherche):
    query = """query ($search: String) {
        Page(perPage: 50) {
            media(search: $search, type: ANIME) {
                id
                title {
                    romaji
                    english
                }
                coverImage {
                    large
                }
            }
        }
    }"""

    donnees = preparer_donnees(
        query, {
            "search": recherche
        }
    )
    requete = creer_requete_anilist(donnees)
    try:
        resultat = executer_requete_anilist(requete)
        if "errors" in resultat:
            print("Erreur AniList :")
            print(resultat["errors"])
            return []
        animes = resultat["data"]["Page"]["media"]
        recherche_lower = recherche.lower()

        # Attribu un score a l'anime pour trier la recherche.
        def score_anime(anime):
            titres = [
                anime["title"]["english"],
                anime["title"]["romaji"]
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
                elif titre.startswith(recherche_lower):
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
                "title": anime["title"],
                "image": anime["coverImage"]["large"]
            }
            for anime in animes[:MAX_SEARCH_RESULTS]
        ]
    except urllib.error.HTTPError as error:
        print(f"Erreur HTTP AniList : {error.code}")
        print(error.read().decode("utf-8"))
        return []
    except urllib.error.URLError as error:
        print("Erreur de connexion à AniList :")
        print(error.reason)
        return []

#  Récupère un anime de la base de donnée.
def recuperer_anime(anime_id):
    query = """query ($id: Int) {
        Media(id: $id, type: ANIME) {
            id
            title {
                romaji
                english
            }
            coverImage {
                large
            }
            description(asHtml: false)
        }
    }"""
    donnees = preparer_donnees(
        query, {
            "id": anime_id
        }
    )
    requete = creer_requete_anilist(donnees)
    try:
        resultat = executer_requete_anilist(requete)
        if "errors" in resultat:
            print(resultat["errors"])
            return None
        media = resultat["data"]["Media"]
        if media is None:
            return None
        titre = (
            media["title"]["english"]
            or media["title"]["romaji"]
        )
        titre_original = (
            media["title"]["romaji"]
            or media["title"]["english"]
        )
        image = media["coverImage"]["large"]
        description = media["description"] or ""
        return {
            "titre": titre,
            "titre_original": titre_original,
            "image": image,
            "description": description
        }
    except Exception as erreur:
        print("Erreur récupération AniList :", erreur)
        return None