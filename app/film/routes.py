from fastapi import APIRouter
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from starlette.requests import Request

from app.config import TEMPLATES_DIR

from app.film.api import (
    rechercher_films,
    recuperer_film,
)

from app.film.database import (
    lister_films,
    modifier_film_vue,
    ajouter_film_complet,
    supprimer_film,
    recuperer_film as recuperer_film_database,
)


templates = Jinja2Templates(directory=TEMPLATES_DIR)

router = APIRouter()


class FilmVueUpdate(BaseModel):
    vue: bool


@router.get(
    "/",
    response_class=HTMLResponse
)
async def index(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="film/index.html",
        context={}
    )


@router.get("/api")
async def get_films():
    return lister_films()


@router.get("/search-film")
async def search_film(q: str):
    return rechercher_films(q)


@router.post("/add-film/{tmdb_id}")
async def add_film(tmdb_id: int):

    film = recuperer_film(tmdb_id)

    if film is None:
        return {
            "success": False
        }

    film_id = ajouter_film_complet(
        titre=film["titre"],
        titre_original=film["titre_original"],
        image=film["image"],
        description=film["description"],
        annee=film["annee"],
        genres=film["genres"],
        duree=film["duree"],
        realisateur=film["realisateur"],
    )

    return {
        "success": True,
        "film_id": film_id
    }


@router.get(
    "/{film_id}",
    response_class=HTMLResponse
)
async def film_page(
    request: Request,
    film_id: int
):

    film = recuperer_film_database(film_id)

    if film is None:
        return HTMLResponse(
            "Film introuvable",
            status_code=404
        )

    return templates.TemplateResponse(
        request=request,
        name="film/film.html",
        context={
            "film": film
        }
    )


@router.put("/films/{film_id}/vue")
async def modifier_vue(
    film_id: int,
    data: FilmVueUpdate
):

    modifier_film_vue(
        film_id,
        data.vue
    )

    return {
        "success": True
    }


@router.delete("/films/{film_id}")
async def delete_film(
    film_id: int
):

    supprimer_film(
        film_id
    )

    return {
        "success": True
    }