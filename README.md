# Anime Library

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
anime-library/
│
├── app/
│   ├── anilist.py
│   └── database.py
│
├── data/
│   └── anime.db
│
├── static/
│   ├── script.js
│   └── style.css
│
├── templates/
│   └── index.html
│
├── main.py
├── seed.py
└── README.md
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

Antoine Fautrel
