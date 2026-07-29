import json
import urllib.request
import urllib.error


ANILIST_API_URL = "https://graphql.anilist.co"


def rechercher_animes(recherche):

    query = """
    query ($search: String) {
        Page(perPage: 50) {
            media(
                search: $search,
                type: ANIME
            ) {
                id
                title {
                    romaji
                    english
                }
                status
            }
        }
    }
    """

    donnees = json.dumps({
        "query": query,
        "variables": {
            "search": recherche
        }
    }).encode("utf-8")


    requete = urllib.request.Request(
        ANILIST_API_URL,
        data=donnees,
        headers={
            "Content-Type": "application/json",
            "Accept": "application/json",
            "User-Agent": "anime-library/1.0"
        },
        method="POST"
    )


    try:

        with urllib.request.urlopen(
            requete,
            timeout=10
        ) as response:

            resultat = json.loads(
                response.read()
            )


        if "errors" in resultat:
            print("Erreur AniList :")
            print(resultat["errors"])

            return []


        animes = resultat["data"]["Page"]["media"]

        print("Resultat recu par Anilist :")

        for anime in animes:
            print(
                anime["title"]["romaji"]
            )

        recherche_lower = recherche.lower()


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

            meilleur_score = 999

            for titre in titres: 

                # Le titre est exactement la recherche
                if titre == recherche_lower:
                    score = 0

                # Le titre commence par la recherche
                elif titre.startswith(recherche_lower):
                    score = 10

                # Le titre contient la recherche
                elif recherche_lower in titre:
                    score = 100

                else:
                    score = 999

                meilleur_score = min(
                    meilleur_score,
                    score
                )

            return meilleur_score


        animes = sorted(
            animes,
            key=score_anime
        )


        return animes[:10]


    except urllib.error.HTTPError as error:

        print(
            f"Erreur HTTP AniList : {error.code}"
        )

        print(
            error.read().decode("utf-8")
        )

        return []


    except urllib.error.URLError as error:

        print(
            "Erreur de connexion à AniList :"
        )

        print(
            error.reason
        )

        return []

def recuperer_anime(anime_id):

    query = """
    query ($id: Int) {
        Media(id: $id, type: ANIME) {
            id

            title {
                romaji
                english
                native
            }

            status

            episodes
        }
    }
    """

    donnees = json.dumps({
        "query": query,
        "variables": {
            "id": anime_id
        }
    }).encode("utf-8")


    requete = urllib.request.Request(
        ANILIST_API_URL,
        data=donnees,
        headers={
            "Content-Type": "application/json",
            "Accept": "application/json",
            "User-Agent": "anime-library/1.0"
        },
        method="POST"
    )


    try:

        with urllib.request.urlopen(
            requete,
            timeout=10
        ) as response:

            resultat = json.loads(
                response.read()
            )


        media = resultat["data"]["Media"]


        return {
            "titre":
                media["title"]["english"]
                or media["title"]["romaji"],

            "titre_original":
                media["title"]["native"],

            "statut":
                media["status"],

            "episodes":
                media["episodes"]
        }


    except Exception as erreur:

        print(
            "Erreur récupération AniList :",
            erreur
        )

        return None
