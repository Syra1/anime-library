from fastapi import APIRouter
from fastapi.responses import HTMLResponse
from starlette.requests import Request
from app.common.database import compter_contenus
from app.config import (TEMPLATES_DIR, templates)
from app.common.media import rechercher_a_voir

# Routeur dédié à la page d'accueil
router = APIRouter()

@router.get("/", response_class=HTMLResponse)
async def index(request: Request):
    contenus = compter_contenus()
    a_voir = rechercher_a_voir()
    return templates.TemplateResponse(
        request=request,
        name="home/index.html",
        context={
            "contenus": contenus,
            "a_voir": a_voir
        }
    )