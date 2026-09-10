# Convertit une liste de valeurs en texte séparé par des virgules.
def convertir_liste_en_texte(elements):
    if not elements:
        return ""

    return ", ".join(str(element) for element in elements)


# Détermine si un média TMDB est un anime ou une série.
def determiner_type_media(media):
    genre_ids = media.get("genre_ids", [])

    if 16 in genre_ids:
        return "anime"

    return "serie"


# Compare les saisons présentes dans la bibliothèque
# avec celles présentes sur TMDB.
def comparer_saisons(saisons_locales, saisons_tmdb):
    return [
        saison
        for saison in saisons_tmdb
        if saison not in saisons_locales
    ]

# Compare les films présents dans la bibliothèque
# avec ceux présents dans une collection TMDB.
def comparer_films_collection(films_locaux, films_tmdb):
    return [
        film
        for film in films_tmdb
        if film["id"] not in films_locaux
    ]

# Recherche les saisons à voir pour toutes les séries.
def rechercher_saisons_series():
    from app.serie.database import lister_series
    from app.serie.database import recuperer_serie

    series = lister_series()
    resultats = []

    for serie in series:
        serie = recuperer_serie(serie["id"])

        if serie is None:
            continue

        saisons_a_voir = [
            saison["numero"]
            for saison in serie["saisons"]
            if not saison["vu"]
        ]

        if saisons_a_voir:
            resultats.append({
                "type": "serie",
                "titre": serie["titre"]
            })

    return resultats

# Recherche les saisons à voir pour tous les anime.
def rechercher_saisons_animes():
    from app.anime.database import lister_animes
    from app.anime.database import recuperer_anime

    animes = lister_animes()
    resultats = []

    for anime in animes:
        anime = recuperer_anime(anime["id"])

        if anime is None:
            continue

        saisons_a_voir = [
            saison["numero"]
            for saison in anime["saisons"]
            if not saison["vu"]
        ]

        if saisons_a_voir:
            resultats.append({
                "type": "anime",
                "titre": anime["titre"]
            })

    return resultats

# Récupère les films présents dans une collection TMDB.
def recuperer_collection(collection_id):
    import urllib.error
    from app.common.tmdb import (
        TMDB_API_URL,
        preparer_parametres,
        creer_requete_tmdb,
        executer_requete_tmdb,
    )

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
        print("Erreur récupération collection TMDB :", repr(erreur))
        return None

# Recherche les films à voir dans toutes les collections.
# Recherche les films à voir dans toutes les collections.
def rechercher_films_collections():
    from app.film.database import lister_films

    films = lister_films()
    resultats = []
    collections_deja_traitees = []

    for film in films:
        collection_id = film["collection_id"]

        if collection_id is None:
            continue

        if collection_id in collections_deja_traitees:
            continue

        collections_deja_traitees.append(collection_id)

        films_tmdb = recuperer_collection(collection_id)

        if films_tmdb is None:
            continue

        films_locaux = [
            film_local["tmdb_id"]
            for film_local in films
            if film_local["collection_id"] == collection_id
        ]

        films_a_voir = comparer_films_collection(
            films_locaux,
            films_tmdb
        )

        if films_a_voir:
            resultats.append({
                "type": "film",
                "collection": film["collection_nom"],
                "films": films_a_voir
            })

    return resultats

# Recherche tous les contenus à voir.
def rechercher_a_voir():
    return {
        "series": rechercher_saisons_series(),
        "animes": rechercher_saisons_animes(),
        "films": rechercher_films_collections()
    }

if __name__ == "__main__":
    resultats = rechercher_a_voir()

    print("Séries à voir :")

    for serie in resultats["series"]:
        print(
            serie["titre"],
            "→ saisons :",
            serie["saisons"]
        )

    print()
    print("Anime à voir :")

    for anime in resultats["animes"]:
        print(
            anime["titre"],
            "→ saisons :",
            anime["saisons"]
        )

    print()
    print("Films à voir :")

    for collection in resultats["films"]:
        print(
            collection["collection"],
            "→ films :"
        )

        for film in collection["films"]:
            print(
                film["title"],
                "→ TMDB :",
                film["id"]
            )