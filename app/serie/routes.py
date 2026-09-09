from fastapi import APIRouter
from fastapi.responses import HTMLResponse
from starlette.requests import Request
from app.common.routes import ajouter_media
from app.config import (TEMPLATES_DIR, templates)
from app.serie.api import (
    rechercher_series,
    recuperer_serie,
)

from app.serie.database import (
    lister_series,
    ajouter_serie,
    supprimer_serie,
    recuperer_serie as recuperer_serie_database,
    modifier_saison_vue_serie,
)

router = APIRouter()

@router.get("/", response_class=HTMLResponse)
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
    return ajouter_media(tmdb_id, recuperer_serie, ajouter_serie, lambda serie: {
        "tmdb_id": serie["id"],
        "titre": serie["titre"],
        "titre_original": serie["titre_original"],
        "image": serie["image"],
        "description": serie["description"],
        "annee": serie["annee"],
        "genres": serie["genres"],
        "duree": serie["duree"],
        "auteur": serie["auteur"],
        "realisateur": serie["realisateur"],
        "nombre_saisons": serie["nombre_saisons"],
        "saisons": serie["saisons"],
    }, "serie_id")

@router.get("/{serie_id}", response_class=HTMLResponse)
async def serie_page(request: Request, serie_id: int):
    serie = recuperer_serie_database(serie_id)

    if serie is None:
        return HTMLResponse("Série introuvable", status_code=404)

    return templates.TemplateResponse(
        request=request,
        name="serie/serie.html",
        context={
            "serie": serie
        }
    )

@router.delete("/series/{serie_id}")
async def delete_serie(serie_id: int):
    supprimer_serie(serie_id)

    return {
        "success": True
    }

@router.post("/{serie_id}/saison/{saison_id}/vu")
async def modifier_vue_serie(serie_id, saison_id, vu: bool):
    modifier_saison_vue_serie(saison_id, vu)

    return {
        "success": True
    }