from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app.config import STATIC_DIR, TEMPLATES_DIR
from app.anime.routes import router as anime_router
# from app.film.routes import router as film_router
# from app.serie.routes import router as serie_router
from app.anime.database import create_tables


app = FastAPI()

# Fichiers statiques
app.mount(
    "/static",
    StaticFiles(directory=STATIC_DIR),
    name="static"
)


# Templates
templates = Jinja2Templates(
    directory=TEMPLATES_DIR
)


# Base de données
create_tables()


# Routes
app.include_router(anime_router)
# app.include_router(film_router)
# app.include_router(serie_router)