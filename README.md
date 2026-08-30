# Bibliothèque Anime/Film/Serie

Une application web développée avec **FastAPI** permettant de créer et gérer sa bibliothèque d'animés.

## Fonctionnalités

* Consultation de sa bibliothèque d'animés
* Gestion des saisons regardées
* Recherche d'animés via l'API AniList
* Affichage des informations principales d'un animé
* Interface web simple en HTML, CSS et JavaScript

## Technologies utilisées

* Python 3
* FastAPI
* SQLite
* Jinja2
* HTML
* CSS
* JavaScript
* API GraphQL AniList

## Structure du projet

```
.
├── app
│   ├── anime
│   │   ├── api.py
│   │   ├── database.py
│   │   ├── __pycache__
│   │   │   ├── api.cpython-314.pyc
│   │   │   ├── database.cpython-314.pyc
│   │   │   └── routes.cpython-314.pyc
│   │   └── routes.py
│   ├── config.py
│   ├── database.py
│   ├── film
│   │   ├── api.py
│   │   ├── database.py
│   │   ├── __pycache__
│   │   │   ├── api.cpython-314.pyc
│   │   │   ├── database.cpython-314.pyc
│   │   │   └── routes.cpython-314.pyc
│   │   └── routes.py
│   ├── home
│   │   ├── __pycache__
│   │   │   └── routes.cpython-314.pyc
│   │   └── routes.py
│   ├── __pycache__
│   │   ├── anilist.cpython-314.pyc
│   │   ├── api.cpython-314.pyc
│   │   ├── config.cpython-314.pyc
│   │   ├── database.cpython-314.pyc
│   │   ├── jikan.cpython-314.pyc
│   │   └── traduction.cpython-314.pyc
│   └── serie
│       ├── api.py
│       ├── database.py
│       ├── __pycache__
│       │   ├── api.cpython-314.pyc
│       │   ├── database.cpython-314.pyc
│       │   └── routes.cpython-314.pyc
│       └── routes.py
├── data
│   └── anime.db
├── main.py
├── __pycache__
│   └── main.cpython-314.pyc
├── README.md
├── requirements.txt
├── static
│   ├── css
│   │   ├── animations.css
│   │   ├── anime
│   │   │   ├── anime.css
│   │   │   └── index.css
│   │   ├── film
│   │   │   ├── film.css
│   │   │   └── index.css
│   │   ├── global.css
│   │   ├── home
│   │   │   └── index.css
│   │   └── serie
│   │       ├── index.css
│   │       └── serie.css
│   ├── icons
│   │   ├── accueil_anime.jpg
│   │   ├── accueil_film.webp
│   │   ├── accueil_serie.jpg
│   │   ├── check.svg
│   │   ├── clapper.svg
│   │   ├── library.svg
│   │   └── search.svg
│   └── js
│       ├── anime
│       │   ├── anime.js
│       │   └── index.js
│       ├── film
│       │   ├── film.js
│       │   └── index.js
│       ├── home
│       │   └── index.js
│       └── serie
│           ├── index.js
│           └── serie.js
└── templates
    ├── anime
    │   ├── anime.html
    │   └── index.html
    ├── base.html
    ├── film
    │   ├── film.html
    │   └── index.html
    ├── home
    │   └── index.html
    └── serie
        ├── index.html
        └── serie.html
```

## Installation

Créer un environnement virtuel :

```bash
python -m venv .venv
```

L'activer :

Linux / macOS :

```bash
source .venv/bin/activate
```

Windows :

```powershell
.venv\Scripts\activate
```

Installer les dépendances :

```bash
pip install -r requirements.txt
```

## Lancer le projet

```bash
python -m uvicorn main:app --reload
```

L'application est ensuite disponible sur :

```
http://127.0.0.1:8000
```

## Fonctionnalités en cours

* Ajout d'un animé à la bibliothèque depuis AniList
* Création automatique des saisons
* Tri intelligent des saisons et contenus spéciaux
* Amélioration de l'interface utilisateur

## Auteur

SYR4
