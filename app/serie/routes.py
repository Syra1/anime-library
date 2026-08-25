from fastapi import APIRouter
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from starlette.requests import Request

from app.config import TEMPLATES_DIR

from app.serie.api import (
    rechercher_series,
    recuperer_serie,
)

from app.serie.database import (
    lister_series,
    ajouter_serie,
    supprimer_serie,
    recuperer_serie as recuperer_serie_database,
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
        name="serie/index.html",
        context={}
    )


@router.get("/api")
async def get_series():
    return lister_series()


@router.get("/search-serie")
async def search_serie(q: str):
    return rechercher_series(q)


@router.post("/add-serie/{tmdb_id}")
async def add_serie(tmdb_id: int):

    serie = recuperer_serie(tmdb_id)

    if serie is None:
        return {
            "success": False
        }

    serie_id = ajouter_serie(
        titre=serie["titre"],
        titre_original=serie["titre_original"],
        image=serie["image"],
        description=serie["description"],
        annee=serie["annee"],
        genres=serie["genres"],
        duree=serie["duree"],
        realisateur=serie["realisateur"],
    )

    return {
        "success": True,
        "serie_id": serie_id
    }


@router.get(
    "/{serie_id}",
    response_class=HTMLResponse
)
async def serie_page(
    request: Request,
    serie_id: int
):

    serie = recuperer_serie_database(serie_id)

    if serie is None:
        return HTMLResponse(
            "Film introuvable",
            status_code=404
        )

    return templates.TemplateResponse(
        request=request,
        name="serie/serie.html",
        context={
            "serie": serie
        }
    )


@router.delete("/series/{serie_id}")
async def delete_serie(
    serie_id: int
):

    supprimer_serie(
        serie_id
    )

    return {
        "success": True
    }