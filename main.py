from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.requests import Request

from app.anilist import (
    rechercher_animes,
    recuperer_anime
)

from app.database import (
    create_tables,
    lister_animes_avec_saisons,
    modifier_saisons_vue,
    ajouter_anime_complet,
    supprimer_anime
)

from pydantic import BaseModel


class SaisonUpdate(BaseModel):
    id: int
    vue: bool


class SaisonBatch(BaseModel):
    saisons: list[SaisonUpdate]


# Créer l'application FastAPI
app = FastAPI()


# Servir les fichiers CSS et JavaScript
app.mount(
    "/static",
    StaticFiles(directory="static"),
    name="static"
)


# Charger les templates HTML
templates = Jinja2Templates(
    directory="templates"
)


# Créer les tables au démarrage
create_tables()


# Page principale
@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={}
    )


# API pour récupérer les animés
@app.get("/animes")
async def get_animes():
    return lister_animes_avec_saisons()

@app.get("/search-anime")
async def search_anime(q: str):
    return rechercher_animes(q)


@app.post("/add-anime/{anilist_id}")
async def add_anime(anilist_id: int):

    anime = recuperer_anime(anilist_id)


    if anime is None:

        return {
            "success": False
        }


    anime_id = ajouter_anime_complet(
        anime["titre"],
        anime["titre_original"],
        anime["statut"],
        anime["episodes"]
    )


    return {
        "success": True,
        "anime_id": anime_id
    }

@app.put("/animes/{anime_id}/saisons")
async def modifier_saisons(
    anime_id: int,
    data: SaisonBatch
):

    modifier_saisons_vue(
        anime_id,
        [
            {
                "id": s.id,
                "vue": s.vue
            }
            for s in data.saisons
        ]
    )

    return {
        "success": True
    }

@app.delete("/animes/{anime_id}")
async def delete_anime(anime_id: int):

    supprimer_anime(anime_id)

    return {
        "success": True
    }
