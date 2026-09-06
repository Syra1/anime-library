import urllib.error
from app.common.tmdb import (
    TMDB_API_URL,
    MAX_SEARCH_RESULTS,
    NO_SCORE,
    IMAGE_BASE_URL,
    preparer_parametres,
    creer_requete_tmdb,
    executer_requete_tmdb,
    rechercher_medias,
    recuperer_media,
)


from app.common.media import (
    convertir_liste_en_texte,
)


# Recherche un film dans la base de données TMDB.
def rechercher_films(recherche):
    return rechercher_medias(
        recherche,
        "search/movie",
        "title",
        "original_title",
        "release_date"
    )


# Récupère un film depuis TMDB.
def recuperer_film(film_id):

    media = recuperer_media(
        film_id,
        "movie"
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
        f"{IMAGE_BASE_URL}{media['poster_path']}"
        if media.get("poster_path")
        else None
    )

    description = media.get("overview") or ""

    annee = None

    if media.get("release_date"):
        annee = int(media["release_date"][:4])

    genres = convertir_liste_en_texte(
        [
            genre["name"]
            for genre in media.get("genres", [])
        ]
    )

    duree = media.get("runtime")

    realisateur = ""

    for personne in media.get("credits", {}).get("crew", []):
        if personne.get("job") == "Director":
            realisateur = personne.get("name")
            break

    collection_id = None
    collection_nom = None

    if media.get("belongs_to_collection"):
        collection_id = media["belongs_to_collection"].get("id")
        collection_nom = media["belongs_to_collection"].get("name")

    return {
        "id": media["id"],
        "titre": titre,
        "titre_original": titre_original,
        "image": image,
        "description": description,
        "annee": annee,
        "genres": genres,
        "duree": duree,
        "realisateur": realisateur,
        "collection_id": collection_id,
        "collection_nom": collection_nom
    }