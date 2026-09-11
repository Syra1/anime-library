from fastapi import APIRouter
from fastapi.responses import HTMLResponse
from starlette.requests import Request
from app.common.routes import ajouter_media
from app.config import (TEMPLATES_DIR, templates)
from app.film.api import (
    rechercher_films,
    recuperer_film,
)
from app.common.media import rechercher_a_voir
from app.film.database import (
    lister_films,
    ajouter_film,
    supprimer_film,
    recuperer_film as recuperer_film_database,
)

router = APIRouter()

@router.get("/", response_class=HTMLResponse)
async def index(request: Request):
    a_voir = rechercher_a_voir()

    noms_a_voir = [
        film["title"]
        for collection in a_voir["films"]
        for film in collection["films"]
    ]

    return templates.TemplateResponse(
        request=request,
        name="film/index.html",
        context={
            "a_voir": noms_a_voir
        }
    )

@router.get("/api")
async def get_films():
    return lister_films()

@router.get("/search-film")
async def search_film(q: str):
    return rechercher_films(q)

@router.post("/add-film/{tmdb_id}")
async def add_film(tmdb_id: int):
    return ajouter_media(tmdb_id, recuperer_film, ajouter_film, lambda film: {
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
    }, "film_id")

@router.get("/{film_id}", response_class=HTMLResponse)
async def film_page(request: Request, film_id: int):
    film = recuperer_film_database(film_id)

    if film is None:
        return HTMLResponse("Film introuvable", status_code=404)

    return templates.TemplateResponse(
        request=request,
        name="film/film.html",
        context={
            "film": film
        }
    )

@router.delete("/films/{film_id}")
async def delete_film(film_id: int):
    supprimer_film(film_id)

    return {
        "success": True
    }