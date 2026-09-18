from app.common.media import MediaManager
from app.common.tmdb import recuperer_collection

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


# ----------------------------------------------------------------------
# Recherche des contenus à voir
# ----------------------------------------------------------------------

# Recherche les saisons à voir pour un type de média.
def rechercher_saisons(type_media):
    media_manager = MediaManager(type_media)

    medias = media_manager.lister_medias()
    resultats = []

    for media in medias:
        media = media_manager.recuperer_media(media["id"])

        if media is None:
            continue

        saisons_a_voir = [
            saison["numero"]
            for saison in media["saisons"]
            if not saison["vu"]
        ]

        if saisons_a_voir:
            resultats.append({
                "type": type_media,
                "titre": media["titre"],
                "image": media["image"],
                "image_secondaire": media["image_secondaire"],
                "saisons": saisons_a_voir,
            })

    return resultats


# Recherche les films à voir dans toutes les collections.
def rechercher_films_collections():
    media_manager = MediaManager("film")

    films = media_manager.lister_medias()

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
            films_tmdb,
        )

        if films_a_voir:
            resultats.append({
                "type": "film",
                "collection": film["collection_nom"],
                "films": films_a_voir,
            })

    return resultats


# Recherche tous les contenus à voir.
def rechercher_a_voir():
    return {
        "series": rechercher_saisons("serie"),
        "animes": rechercher_saisons("anime"),
        "films": rechercher_films_collections(),
    }