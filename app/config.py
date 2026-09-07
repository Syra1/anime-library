from pathlib import Path
import os
from dotenv import load_dotenv

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
TMDB_ACCESS_TOKEN = os.getenv(
    "TMDB_ACCESS_TOKEN"
)