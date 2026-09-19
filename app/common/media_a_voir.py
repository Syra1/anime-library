from app.common.media import MediaManager
from app.common.tmdb import recuperer_collection

# ----------------------------------------------------------------------
# Recherche des contenus à voir
# ----------------------------------------------------------------------

# Recherche les saisons à voir pour un type de média.
def rechercher_saisons(type_media):
    media_manager = MediaManager(type_media)

    medias = media_manager.lister_medias(avec_saisons=True)
    resultats = []

    for media in medias:
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
#
# Renvoie une liste plate (un film = une entrée), avec le même
# format que rechercher_saisons (type, titre, image, image_secondaire),
# plus le nom de la collection dont il fait partie.
def rechercher_films_collections():
    media_manager = MediaManager("film")

    films = media_manager.lister_medias()

    resultats = []
    collections_deja_traitees = set()

    for film in films:
        collection_id = film["collection_id"]

        if collection_id is None:
            continue

        if collection_id in collections_deja_traitees:
            continue

        collections_deja_traitees.add(collection_id)

        films_tmdb = recuperer_collection(collection_id)

        if films_tmdb is None:
            continue

        films_locaux = {
            film_local["tmdb_id"]
            for film_local in films
            if film_local["collection_id"] == collection_id
        }

        for film_tmdb in films_tmdb:
            if film_tmdb["id"] in films_locaux:
                continue

            resultats.append({
                "type": "film",
                "titre": film_tmdb["titre"],
                "image": film_tmdb["image"],
                "image_secondaire": film_tmdb["image_secondaire"],
                "collection": film["collection_nom"],
            })

    return resultats


# Recherche tous les contenus à voir.
def rechercher_a_voir():
    return {
        "series": rechercher_saisons("serie"),
        "animes": rechercher_saisons("anime"),
        "films": rechercher_films_collections(),
    }