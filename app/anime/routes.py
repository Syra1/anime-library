from fastapi import APIRouter
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from starlette.requests import Request
from app.common.routes import ajouter_media

from app.config import TEMPLATES_DIR

from app.anime.api import (
    rechercher_animes,
    recuperer_anime,
)

from app.anime.database import (
    lister_animes,
    ajouter_anime,
    supprimer_anime,
    recuperer_anime as recuperer_anime_database,
)


templates = Jinja2Templates(directory=TEMPLATES_DIR)

router = APIRouter()

@router.get(
    "/",
    response_class=HTMLResponse
)
async def index(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="anime/index.html",
        context={}
    )


@router.get("/api")
async def get_animes():
    return lister_animes()


@router.get("/search-anime")
async def search_anime(q: str):
    return rechercher_animes(q)


@router.post("/add-anime/{tmdb_id}")
async def add_anime(tmdb_id: int):
    return ajouter_media(tmdb_id, recuperer_anime, ajouter_anime, lambda anime: {
        "titre": anime["titre"],
        "titre_original": anime["titre_original"],
        "image": anime["image"],
        "description": anime["description"],
        "annee": anime["annee"],
        "genres": anime["genres"],
        "duree": anime["duree"],
        "auteur": anime["auteur"],
        "realisateur": anime["realisateur"],
        "nombre_saisons": anime["nombre_saisons"],
        "saisons": anime["saisons"],
    })


@router.get(
    "/{anime_id}",
    response_class=HTMLResponse
)
async def anime_page(
    request: Request,
    anime_id: int
):

    anime = recuperer_anime_database(anime_id)

    if anime is None:
        return HTMLResponse(
            "Anime introuvable",
            status_code=404
        )

    return templates.TemplateResponse(
        request=request,
        name="anime/anime.html",
        context={
            "anime": anime
        }
    )


@router.delete("/animes/{anime_id}")
async def delete_anime(
    anime_id: int
):

    supprimer_anime(
        anime_id
    )

    return {
        "success": True
    }