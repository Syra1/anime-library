from fastapi import APIRouter
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from starlette.requests import Request

from app.config import TEMPLATES_DIR


templates = Jinja2Templates(
    directory=TEMPLATES_DIR
)

# Routeur dédié à la page d'accueil
router = APIRouter()

@router.get(
    "/",
    response_class=HTMLResponse
)
async def index(request: Request):

    return templates.TemplateResponse(
        request=request,
        name="home/index.html",
        context={}
    )