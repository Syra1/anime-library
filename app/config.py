from pathlib import Path
import os
from dotenv import load_dotenv
from fastapi.templating import Jinja2Templates

# Racine du projet
BASE_DIR = Path(__file__).resolve().parent.parent

# Dossiers du projet
TEMPLATES_DIR = BASE_DIR / "templates"
STATIC_DIR = BASE_DIR / "static"
DATABASE_PATH = BASE_DIR / "data" / "anime.db"

# Fichier .env
ENV_FILE = BASE_DIR / ".env"
load_dotenv(ENV_FILE)

# Token TMDB
TMDB_ACCESS_TOKEN = os.getenv("TMDB_ACCESS_TOKEN")

# Définit le dossier contenant les templates HTML.
templates = Jinja2Templates(directory=TEMPLATES_DIR)





TMDB_API_URL = "https://api.themoviedb.org/3"
TMDB_HEADERS = {
    "Authorization": f"Bearer {TMDB_ACCESS_TOKEN}",
    "Accept": "application/json"
}

TMDB_TIMEOUT = 10
MAX_SEARCH_RESULTS = 20
IMAGE_BASE_URL = "https://image.tmdb.org/t/p/w500"