from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates


def ajouter_media(tmdb_id, recuperer_media, ajouter_media, donnees):
    media = recuperer_media(tmdb_id)

    if media is None:
        return {
            "success": False
        }

    media_id = ajouter_media(**donnees(media))

    return {
        "success": True,
        "media_id": media_id
    }