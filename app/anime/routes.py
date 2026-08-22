from fastapi import APIRouter
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, Field
from starlette.requests import Request
from app.config import TEMPLATES_DIR

from app.anime.api import (
    rechercher_animes,
    recuperer_anime,
)

from app.anime.database import (
    lister_animes_avec_saisons,
    modifier_saisons_vue,
    ajouter_anime_complet,
    supprimer_anime,
    recuperer_anime_avec_saisons,
    ajouter_saison_suivante,
    supprimer_derniere_saison,
)

templates = Jinja2Templates(
    directory=TEMPLATES_DIR
)

router = APIRouter()

class SaisonUpdate(BaseModel):
    id: int
    vue: bool


class SaisonBatch(BaseModel):
    saisons: list[SaisonUpdate]


class AnimeAdd(BaseModel):
    nombre_saisons: int = Field(
        ge=1,
        le=30
    )


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


@router.get(
    "/anime/{anime_id}",
    response_class=HTMLResponse
)
async def anime_page(
    request: Request,
    anime_id: int
):

    anime = recuperer_anime_avec_saisons(
        anime_id
    )

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

@router.get("/animes")
async def get_animes():

    return lister_animes_avec_saisons()


@router.get("/search-anime")
async def search_anime(q: str):

    return rechercher_animes(q)


@router.post("/add-anime/{anilist_id}")
async def add_anime(
    anilist_id: int,
    data: AnimeAdd,
):

    anime = recuperer_anime(
        anilist_id
    )

    if anime is None:
        return {
            "success": False
        }

    anime_id = ajouter_anime_complet(
        titre=anime["titre"],
        titre_original=anime["titre_original"],
        image=anime["image"],
        nombre_saisons=data.nombre_saisons,
        description=anime["description"],
    )

    return {
        "success": True,
        "anime_id": anime_id
    }


@router.put("/animes/{anime_id}/saisons")
async def modifier_saisons(
    anime_id: int,
    data: SaisonBatch
):

    modifier_saisons_vue(
        anime_id,
        [
            {
                "id": saison.id,
                "vue": saison.vue
            }
            for saison in data.saisons
        ]
    )

    return {
        "success": True
    }


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


@router.post("/animes/{anime_id}/saisons/ajouter")
async def ajouter_saison(
    anime_id: int
):

    saison = ajouter_saison_suivante(
        anime_id
    )

    return {
        "success": True,
        "saison": saison
    }


@router.delete("/animes/{anime_id}/saisons/retirer")
async def retirer_saison(
    anime_id: int
):

    success = supprimer_derniere_saison(
        anime_id
    )

    return {
        "success": success
    }