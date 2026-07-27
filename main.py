from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.requests import Request

from app.database import (
    create_tables,
    lister_animes_avec_saisons,
    modifier_saison_vue
)


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

@app.put("/animes/{anime_id}/saisons/{saison_id}")
async def modifier_vue_saison(
    anime_id: int,
    saison_id: int,
    vue: bool
):
    modifier_saison_vue(
        anime_id,
        saison_id,
        vue
    )

    return {
        "success": True,
        "anime_id": anime_id,
        "saison_id": saison_id,
        "vue": vue
    }
