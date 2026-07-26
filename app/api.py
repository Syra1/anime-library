from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles

from app.database import lister_animes


app = FastAPI()


app.mount(
    "/static",
    StaticFiles(directory="static"),
    name="static"
)


@app.get("/", response_class=HTMLResponse)
def accueil():
    with open("templates/index.html", "r", encoding="utf-8") as fichier:
        return fichier.read()


@app.get("/animes")
def get_animes():
    animes = lister_animes()

    return [
        {
            "id": anime[0],
            "titre": anime[1],
            "titre_original": anime[2],
            "vu": bool(anime[3])
        }
        for anime in animes
    ]
