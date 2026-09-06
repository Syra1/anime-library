from app.common.tmdb import (
    TMDB_API_URL,
    MAX_SEARCH_RESULTS,
    NO_SCORE,
    IMAGE_BASE_URL,
    preparer_parametres,
    creer_requete_tmdb,
    executer_requete_tmdb,
)


from app.common.media import (
    convertir_liste_en_texte,
)


# Recherche un film dans la base de données TMDB.
def rechercher_films(recherche):
    parametres = preparer_parametres({
        "query": recherche,
        "language": "fr-FR",
        "region": "FR",
        "include_adult": "false",
        "page": 1
    })

    url = (
        f"{TMDB_API_URL}/search/movie?"
        f"{parametres}"
    )

    requete = creer_requete_tmdb(url)

    try:
        resultat = executer_requete_tmdb(
            requete
        )

        films = resultat.get(
            "results",
            []
        )

        recherche_lower = recherche.lower()

        # Attribue un score au film
        # pour trier la recherche.
        def score_film(film):
            titres = [
                film.get("title"),
                film.get("original_title")
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

        films = sorted(
            films,
            key=score_film
        )

        return [
            {
                "id": film["id"],

                "title": film.get(
                    "title"
                ),

                "original_title": film.get(
                    "original_title"
                ),

                "image": (
                    f"{IMAGE_BASE_URL}"
                    f"{film['poster_path']}"
                    if film.get("poster_path")
                    else None
                ),

                "annee": (
                    film["release_date"][:4]
                    if film.get("release_date")
                    else None
                )
            }
            for film in films[:MAX_SEARCH_RESULTS]
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


# Récupère un film depuis TMDB.
def recuperer_film(film_id):
    parametres = preparer_parametres({
        "language": "fr-FR",
        "append_to_response": "credits"
    })

    url = (
        f"{TMDB_API_URL}/movie/"
        f"{film_id}?{parametres}"
    )

    requete = creer_requete_tmdb(url)

    try:
        media = executer_requete_tmdb(
            requete
        )

        if not media:
            return None

        titre = (
            media.get("title")
            or media.get("original_title")
        )

        titre_original = (
            media.get("original_title")
            or media.get("title")
        )

        image = (
            f"{IMAGE_BASE_URL}"
            f"{media['poster_path']}"
            if media.get("poster_path")
            else None
        )

        description = (
            media.get("overview")
            or ""
        )

        annee = None

        if media.get("release_date"):
            annee = int(
                media["release_date"][:4]
            )

        genres = convertir_liste_en_texte(
            [
                genre["name"]
                for genre in media.get(
                    "genres",
                    []
                )
            ]
        )

        duree = media.get("runtime")

        realisateur = None

        collection_id = None
        collection_nom = None

        collection = media.get(
            "belongs_to_collection"
        )

        if collection:
            collection_id = collection.get("id")
            collection_nom = collection.get("name")

        credits = media.get(
            "credits",
            {}
        )

        crew = credits.get(
            "crew",
            []
        )

        for personne in crew:
            if personne.get("job") == "Director":
                realisateur = personne.get("name")
                break

        return {
            "titre": titre,
            "titre_original": titre_original,
            "image": image,
            "description": description,
            "annee": annee,
            "genres": genres,
            "duree": duree,
            "realisateur": realisateur,
            "collection_id": collection_id,
            "collection_nom": collection_nom,

        }

    except urllib.error.HTTPError as error:
        print(
            f"Erreur HTTP TMDB : {error.code}"
        )

        print(
            error.read().decode("utf-8")
        )

        return None

    except urllib.error.URLError as error:
        print(
            "Erreur de connexion à TMDB :"
        )

        print(error.reason)

        return None

    except TimeoutError:
        print(
            "TMDB a mis trop de temps à répondre."
        )

        return None

    except Exception as erreur:
        print(
            "Erreur récupération TMDB :",
            erreur
        )

        return None