from fastapi import APIRouter
from fastapi.responses import HTMLResponse
from starlette.requests import Request

from app.config import templates
from app.common.media import MediaManager
from app.common.media_a_voir import rechercher_a_voir
from app.anime.api import (
    rechercher_animes,
    recuperer_anime,
)

from app.film.api import (
    rechercher_films,
    recuperer_film,
)

from app.serie.api import (
    rechercher_series,
    recuperer_serie,
)


def ajouter_media(
    tmdb_id,
    recuperer_media,
    ajouter_media_database,
    donnees,
    nom_id,
):
    media = recuperer_media(tmdb_id)

    if media is None:
        return {
            "success": False
        }

    media_id = ajouter_media_database(**donnees(media))

    return {
        "success": True,
        nom_id: media_id
    }


def creer_router_media(
    type_media,
    rechercher,
    recuperer,
    template,
    donnees,
    nom_id,
    chemin_suppression,
    cle_a_voir,
):
    router = APIRouter()
    media = MediaManager(type_media)

    # Page d'accueil du média
    @router.get("/", response_class=HTMLResponse)
    async def index(request: Request):
        a_voir = rechercher_a_voir()

        if type_media == "film":
            noms_a_voir = [
                film["title"]
                for collection in a_voir["films"]
                for film in collection["films"]
            ]
        else:
            noms_a_voir = [
                contenu["titre"]
                for contenu in a_voir[cle_a_voir]
            ]

        return templates.TemplateResponse(
            request=request,
            name=f"{template}/index.html",
            context={
                "a_voir": noms_a_voir
            }
        )

    # API : liste des médias
    @router.get("/api")
    async def get_medias():
        return media.lister_medias()

    # Recherche TMDB
    @router.get(f"/search-{type_media}")
    async def search_media(q: str):
        return rechercher(q)

    # Ajouter un média depuis TMDB
    @router.post(f"/add-{type_media}/{{tmdb_id}}")
    async def add_media(tmdb_id: int):
        return ajouter_media(
            tmdb_id,
            recuperer,
            media.ajouter_media,
            donnees,
            nom_id,
        )

    # Page d'un média
    @router.get("/{media_id}", response_class=HTMLResponse)
    async def media_page(
        request: Request,
        media_id: int,
    ):
        media_data = media.recuperer_media(media_id)

        if media_data is None:
            return HTMLResponse(
                f"{type_media.capitalize()} introuvable",
                status_code=404
            )

        return templates.TemplateResponse(
            request=request,
            name=f"{template}/{template}.html",
            context={
                type_media: media_data
            }
        )

    # Supprimer un média
    @router.delete(f"/{chemin_suppression}/{{media_id}}")
    async def delete_media(media_id: int):
        media.supprimer_media(media_id)

        return {
            "success": True
        }

    # Modifier les saisons vues
    if type_media in ("serie", "anime"):

        @router.post("/{media_id}/saisons/vu")
        async def modifier_vue(
            media_id: int,
            saisons_ids: list[int],
            vu: bool,
        ):
            media.modifier_saison_vue(
                saisons_ids,
                vu
            )

            return {
                "success": True
            }

    return router


# ---------------------------------------------------------
# Données à enregistrer en base
# ---------------------------------------------------------

def donnees_film(film):
    return {
        "tmdb_id": film["id"],
        "titre": film["titre"],
        "titre_original": film["titre_original"],
        "image": film["image"],
        "description": film["description"],
        "annee": film["annee"],
        "genres": film["genres"],
        "duree": film["duree"],
        "auteur": film["auteur"],
        "realisateur": film["realisateur"],
        "collection_id": film["collection_id"],
        "collection_nom": film["collection_nom"],
    }


def donnees_serie(serie):
    return {
        "tmdb_id": serie["id"],
        "titre": serie["titre"],
        "titre_original": serie["titre_original"],
        "image": serie["image"],
        "image_secondaire": serie["image_secondaire"],
        "description": serie["description"],
        "annee": serie["annee"],
        "genres": serie["genres"],
        "duree": serie["duree"],
        "auteur": serie["auteur"],
        "realisateur": serie["realisateur"],
        "nombre_saisons": serie["nombre_saisons"],
        "saisons": serie["saisons"],
    }


def donnees_anime(anime):
    return {
        "tmdb_id": anime["id"],
        "titre": anime["titre"],
        "titre_original": anime["titre_original"],
        "image": anime["image"],
        "image_secondaire": anime["image_secondaire"],
        "description": anime["description"],
        "annee": anime["annee"],
        "genres": anime["genres"],
        "duree": anime["duree"],
        "auteur": anime["auteur"],
        "realisateur": anime["realisateur"],
        "nombre_saisons": anime["nombre_saisons"],
        "saisons": anime["saisons"],
    }


# ---------------------------------------------------------
# Routeurs
# ---------------------------------------------------------

anime_router = creer_router_media(
    type_media="anime",
    rechercher=rechercher_animes,
    recuperer=recuperer_anime,
    template="anime",
    donnees=donnees_anime,
    nom_id="anime_id",
    chemin_suppression="animes",
    cle_a_voir="animes",
)


film_router = creer_router_media(
    type_media="film",
    rechercher=rechercher_films,
    recuperer=recuperer_film,
    template="film",
    donnees=donnees_film,
    nom_id="film_id",
    chemin_suppression="films",
    cle_a_voir="films",
)


serie_router = creer_router_media(
    type_media="serie",
    rechercher=rechercher_series,
    recuperer=recuperer_serie,
    template="serie",
    donnees=donnees_serie,
    nom_id="serie_id",
    chemin_suppression="series",
    cle_a_voir="series",
)