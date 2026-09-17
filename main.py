from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.config import STATIC_DIR
from app.home.routes import router as home_router

from app.common.media import MediaManager
from app.common.route_media import (
    anime_router,
    film_router,
    serie_router,
)


app = FastAPI()


# Fichiers statiques
app.mount(
    "/static",
    StaticFiles(directory=STATIC_DIR),
    name="static"
)


# Base de données
MediaManager.create_tables()


# Routes
app.include_router(home_router)

app.include_router(anime_router, prefix="/anime")
app.include_router(film_router, prefix="/film")
app.include_router(serie_router, prefix="/serie")