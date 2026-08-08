from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.requests import Request
from pydantic import BaseModel, Field
from app.anilist import (
    rechercher_animes,
    recuperer_anime
)
from app.database import (
    create_tables,
    lister_animes_avec_saisons,
    modifier_saisons_vue,
    ajouter_anime_complet,
    supprimer_anime,
    recuperer_anime_avec_saisons
)
from pathlib import Path

# Debut du code
BASE_DIR = Path(__file__).resolve().parent

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

# Créer l'application FastAPI
app = FastAPI()


# Servir les fichiers CSS et JavaScript
app.mount(
    "/static",
    StaticFiles(directory=BASE_DIR / "static"),
    name="static"
)


# Charger les templates HTML
templates = Jinja2Templates(
    directory=BASE_DIR / "templates"
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

# Page détail d'un anime
@app.get("/anime", response_class=HTMLResponse)
async def anime_page(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="anime.html",
        context={}
    )


@app.get("/anime/{anime_id}", response_class=HTMLResponse)
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
        name="anime.html",
        context={
            "anime": anime
        }
    )

# API pour récupérer les animés
@app.get("/animes")
async def get_animes():
    return lister_animes_avec_saisons()

@app.get("/search-anime")
async def search_anime(q: str):
    return rechercher_animes(q)


@app.post("/add-anime/{anilist_id}")
async def add_anime(
    anilist_id: int,
    data: AnimeAdd
):

    anime = recuperer_anime(anilist_id)


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
        nombre_episodes=anime["nombre_episodes"]
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
