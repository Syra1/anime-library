import urllib.error

from app.common.database import (
    get_connection,
    execute_query,
    fetch_all,
    fetch_one,
    modifier_saison_vue as modifier_saison_vue_database,
    creer_suivi_media,
)


# Configuration des différents types de médias.
#
# Le type est défini une seule fois lors de la création
# du MediaManager.
MEDIA_CONFIG = {
    "film": {
        "table": "film",
        "avec_saisons": False,
        "avec_collection": True,
    },
    "serie": {
        "table": "serie",
        "table_saison": "saison_serie",
        "id_saison": "serie_id",
        "avec_saisons": True,
        "avec_collection": False,
    },
    "anime": {
        "table": "anime",
        "table_saison": "saison_anime",
        "id_saison": "anime_id",
        "avec_saisons": True,
        "avec_collection": False,
    },
}


# Vérifie qu'un type de média est valide.
def _get_config(type_media):
    if type_media not in MEDIA_CONFIG:
        raise ValueError(
            f"Type de média invalide : {type_media}. "
            f"Valeurs acceptées : {', '.join(MEDIA_CONFIG.keys())}"
        )

    return MEDIA_CONFIG[type_media]


class MediaManager:

    def __init__(self, type_media):
        self.type_media = type_media
        self.config = _get_config(type_media)

    # ------------------------------------------------------------------
    # Création des tables
    # ------------------------------------------------------------------

    @staticmethod
    def create_tables():
        connection = get_connection()

        # Table des films.
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS film (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                tmdb_id INTEGER NOT NULL,
                titre TEXT NOT NULL,
                titre_original TEXT,
                image TEXT,
                description TEXT,
                annee INTEGER,
                genres TEXT,
                duree INTEGER,
                auteur TEXT,
                realisateur TEXT,
                collection_id INTEGER,
                collection_nom TEXT
            )
            """
        )

        # Table des séries.
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS serie (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                tmdb_id INTEGER NOT NULL,
                titre TEXT NOT NULL,
                titre_original TEXT,
                image TEXT,
                image_secondaire TEXT,
                description TEXT,
                annee INTEGER,
                genres TEXT,
                duree INTEGER,
                auteur TEXT,
                realisateur TEXT,
                nombre_saisons INTEGER
            )
            """
        )

        # Saisons des séries.
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS saison_serie (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                serie_id INTEGER NOT NULL,
                titre TEXT,
                numero INTEGER NOT NULL,
                nombre_episodes INTEGER NOT NULL,
                vu INTEGER NOT NULL DEFAULT 0,
                FOREIGN KEY (serie_id)
                    REFERENCES serie(id)
                    ON DELETE CASCADE
            )
            """
        )

        # Table des anime.
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS anime (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                tmdb_id INTEGER NOT NULL,
                titre TEXT NOT NULL,
                titre_original TEXT,
                image TEXT,
                image_secondaire TEXT,
                description TEXT,
                annee INTEGER,
                genres TEXT,
                duree INTEGER,
                auteur TEXT,
                realisateur TEXT,
                nombre_saisons INTEGER
            )
            """
        )

        # Saisons des anime.
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS saison_anime (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                anime_id INTEGER NOT NULL,
                titre TEXT,
                numero INTEGER NOT NULL,
                nombre_episodes INTEGER NOT NULL,
                vu INTEGER NOT NULL DEFAULT 0,
                FOREIGN KEY (anime_id)
                    REFERENCES anime(id)
                    ON DELETE CASCADE
            )
            """
        )

        connection.commit()
        connection.close()

    # ------------------------------------------------------------------
    # Ajout d'un média
    # ------------------------------------------------------------------

    def ajouter_media(self, **donnees):
        if self.type_media == "film":
            return self._ajouter_film(donnees)

        return self._ajouter_media_avec_saisons(donnees)

    def _ajouter_film(self, donnees):
        cursor = execute_query(
            """
            INSERT INTO film (
                tmdb_id,
                titre,
                titre_original,
                image,
                description,
                annee,
                genres,
                duree,
                auteur,
                realisateur,
                collection_id,
                collection_nom
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                donnees.get("tmdb_id"),
                donnees.get("titre"),
                donnees.get("titre_original"),
                donnees.get("image"),
                donnees.get("description"),
                donnees.get("annee"),
                donnees.get("genres"),
                donnees.get("duree"),
                donnees.get("auteur"),
                donnees.get("realisateur"),
                donnees.get("collection_id"),
                donnees.get("collection_nom"),
            ),
        )

        return cursor.lastrowid

    def _ajouter_media_avec_saisons(self, donnees):
        table = self.config["table"]
        table_saison = self.config["table_saison"]
        id_saison = self.config["id_saison"]

        cursor = execute_query(
            f"""
            INSERT INTO {table} (
                tmdb_id,
                titre,
                titre_original,
                image,
                image_secondaire,
                description,
                annee,
                genres,
                duree,
                auteur,
                realisateur,
                nombre_saisons
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                donnees.get("tmdb_id"),
                donnees.get("titre"),
                donnees.get("titre_original"),
                donnees.get("image"),
                donnees.get("image_secondaire"),
                donnees.get("description"),
                donnees.get("annee"),
                donnees.get("genres"),
                donnees.get("duree"),
                donnees.get("auteur"),
                donnees.get("realisateur"),
                donnees.get("nombre_saisons"),
            ),
        )

        media_id = cursor.lastrowid

        for saison in donnees.get("saisons", []):
            execute_query(
                f"""
                INSERT INTO {table_saison} (
                    {id_saison},
                    titre,
                    numero,
                    nombre_episodes
                )
                VALUES (?, ?, ?, ?)
                """,
                (
                    media_id,
                    saison["titre"],
                    saison["numero"],
                    saison["nombre_episodes"],
                ),
            )

        return media_id

    # ------------------------------------------------------------------
    # Liste des médias
    # ------------------------------------------------------------------

    def lister_medias(self):
        if self.type_media == "film":
            return self._lister_films()

        return self._lister_medias_avec_saisons()

    def _lister_films(self):
        films = fetch_all(
            """
            SELECT
                film.id,
                film.tmdb_id,
                film.titre,
                film.titre_original,
                film.image,
                film.description,
                film.annee,
                film.genres,
                film.duree,
                film.auteur,
                film.realisateur,
                film.collection_id,
                film.collection_nom
            FROM film
            ORDER BY
                COALESCE(
                    film.collection_nom,
                    film.titre
                ) COLLATE NOCASE ASC,
                film.annee ASC,
                film.titre COLLATE NOCASE ASC
            """
        )

        suivis = self._creer_suivis_collections(films)

        return [
            {
                "id": film["id"],
                "tmdb_id": film["tmdb_id"],
                "titre": film["titre"],
                "titre_original": film["titre_original"],
                "image": film["image"],
                "description": film["description"],
                "annee": film["annee"],
                "genres": film["genres"],
                "duree": film["duree"],
                "auteur": film["auteur"],
                "realisateur": film["realisateur"],
                "collection_id": film["collection_id"],
                "collection_nom": film["collection_nom"],
                "suivi": suivis.get(film["collection_id"]),
            }
            for film in films
        ]

    def _lister_medias_avec_saisons(self):
        table = self.config["table"]

        medias = fetch_all(
            f"""
            SELECT
                {table}.id,
                {table}.tmdb_id,
                {table}.titre,
                {table}.titre_original,
                {table}.image,
                {table}.image_secondaire,
                {table}.description,
                {table}.annee,
                {table}.genres,
                {table}.duree,
                {table}.auteur,
                {table}.realisateur,
                {table}.nombre_saisons
            FROM {table}
            ORDER BY
                {table}.titre COLLATE NOCASE ASC,
                {table}.annee ASC
            """
        )

        return [
            {
                "id": media["id"],
                "tmdb_id": media["tmdb_id"],
                "titre": media["titre"],
                "titre_original": media["titre_original"],
                "image": media["image"],
                "image_secondaire": media["image_secondaire"],
                "description": media["description"],
                "annee": media["annee"],
                "genres": media["genres"],
                "duree": media["duree"],
                "auteur": media["auteur"],
                "realisateur": media["realisateur"],
                "nombre_saisons": media["nombre_saisons"],
                "suivi": creer_suivi_media(
                    self.compter_saisons_vues(media["id"]),
                    media["nombre_saisons"],
                ),
            }
            for media in medias
        ]

    # ------------------------------------------------------------------
    # Collections de films
    # ------------------------------------------------------------------

    def _creer_suivis_collections(self, films):
        suivis = {}
        collections_deja_traitees = []

        for film in films:
            collection_id = film["collection_id"]

            if collection_id is None:
                continue

            if collection_id in collections_deja_traitees:
                continue

            collections_deja_traitees.append(collection_id)

            films_tmdb = recuperer_collection(collection_id)

            if films_tmdb is None:
                continue

            films_locaux = [
                film_local
                for film_local in films
                if film_local["collection_id"] == collection_id
            ]

            suivis[collection_id] = creer_suivi_media(
                len(films_locaux),
                len(films_tmdb),
            )

        return suivis

    # ------------------------------------------------------------------
    # Récupération d'un média
    # ------------------------------------------------------------------

    def recuperer_media(self, media_id):
        if self.type_media == "film":
            return self._recuperer_film(media_id)

        return self._recuperer_media_avec_saisons(media_id)

    def _recuperer_film(self, film_id):
        film = fetch_one(
            """
            SELECT
                film.id,
                film.tmdb_id,
                film.titre,
                film.titre_original,
                film.image,
                film.description,
                film.annee,
                film.genres,
                film.duree,
                film.auteur,
                film.realisateur,
                film.collection_id,
                film.collection_nom
            FROM film
            WHERE film.id = ?
            """,
            (film_id,),
        )

        if film is None:
            return None

        return {
            "id": film["id"],
            "tmdb_id": film["tmdb_id"],
            "titre": film["titre"],
            "titre_original": film["titre_original"],
            "image": film["image"],
            "description": film["description"],
            "annee": film["annee"],
            "genres": film["genres"],
            "duree": film["duree"],
            "auteur": film["auteur"],
            "realisateur": film["realisateur"],
            "collection_id": film["collection_id"],
            "collection_nom": film["collection_nom"],
        }

    def _recuperer_media_avec_saisons(self, media_id):
        table = self.config["table"]
        table_saison = self.config["table_saison"]
        id_saison = self.config["id_saison"]

        media = fetch_one(
            f"""
            SELECT
                {table}.id,
                {table}.tmdb_id,
                {table}.titre,
                {table}.titre_original,
                {table}.image,
                {table}.image_secondaire,
                {table}.description,
                {table}.annee,
                {table}.genres,
                {table}.duree,
                {table}.auteur,
                {table}.realisateur,
                {table}.nombre_saisons
            FROM {table}
            WHERE {table}.id = ?
            """,
            (media_id,),
        )

        if media is None:
            return None

        saisons = fetch_all(
            f"""
            SELECT
                id,
                titre,
                numero,
                nombre_episodes,
                vu
            FROM {table_saison}
            WHERE {id_saison} = ?
            ORDER BY numero ASC
            """,
            (media_id,),
        )

        return {
            "id": media["id"],
            "tmdb_id": media["tmdb_id"],
            "titre": media["titre"],
            "titre_original": media["titre_original"],
            "image": media["image"],
            "image_secondaire": media["image_secondaire"],
            "description": media["description"],
            "annee": media["annee"],
            "genres": media["genres"],
            "duree": media["duree"],
            "auteur": media["auteur"],
            "realisateur": media["realisateur"],
            "nombre_saisons": media["nombre_saisons"],
            "saisons": [
                {
                    "id": saison["id"],
                    "titre": saison["titre"],
                    "numero": saison["numero"],
                    "nombre_episodes": saison["nombre_episodes"],
                    "vu": saison["vu"],
                }
                for saison in saisons
            ],
        }

    # ------------------------------------------------------------------
    # Suppression
    # ------------------------------------------------------------------

    def supprimer_media(self, media_id):
        table = self.config["table"]

        execute_query(
            f"""
            DELETE FROM {table}
            WHERE id = ?
            """,
            (media_id,),
        )

    # ------------------------------------------------------------------
    # Gestion des saisons
    # ------------------------------------------------------------------

    def compter_saisons_vues(self, media_id):
        if not self.config["avec_saisons"]:
            raise ValueError(
                f"Le média '{self.type_media}' ne possède pas de saisons."
            )

        table_saison = self.config["table_saison"]
        id_saison = self.config["id_saison"]

        saisons = fetch_all(
            f"""
            SELECT vu
            FROM {table_saison}
            WHERE {id_saison} = ?
            """,
            (media_id,),
        )

        return sum(
            saison["vu"]
            for saison in saisons
        )

    def modifier_saison_vue(self, saisons_ids, vu):
        if not self.config["avec_saisons"]:
            raise ValueError(
                f"Le média '{self.type_media}' ne possède pas de saisons."
            )

        modifier_saison_vue_database(
            self.type_media,
            saisons_ids,
            vu,
        )


# ----------------------------------------------------------------------
# Fonctions utilitaires
# ----------------------------------------------------------------------

# Convertit une liste de valeurs en texte séparé par des virgules.
def convertir_liste_en_texte(elements):
    if not elements:
        return ""

    return ", ".join(str(element) for element in elements)


# Détermine si un média TMDB est un anime ou une série.
def determiner_type_media(media):
    genre_ids = media.get("genre_ids", [])

    if 16 in genre_ids:
        return "anime"

    return "serie"


# Compare les saisons présentes dans la bibliothèque
# avec celles présentes sur TMDB.
def comparer_saisons(saisons_locales, saisons_tmdb):
    return [
        saison
        for saison in saisons_tmdb
        if saison not in saisons_locales
    ]


# Compare les films présents dans la bibliothèque
# avec ceux présents dans une collection TMDB.
def comparer_films_collection(films_locaux, films_tmdb):
    return [
        film
        for film in films_tmdb
        if film["id"] not in films_locaux
    ]


# ----------------------------------------------------------------------
# Recherche des contenus à voir
# ----------------------------------------------------------------------

# Recherche les saisons à voir pour un type de média.
def rechercher_saisons(type_media):
    media_manager = MediaManager(type_media)

    medias = media_manager.lister_medias()
    resultats = []

    for media in medias:
        media = media_manager.recuperer_media(media["id"])

        if media is None:
            continue

        saisons_a_voir = [
            saison["numero"]
            for saison in media["saisons"]
            if not saison["vu"]
        ]

        if saisons_a_voir:
            resultats.append({
                "type": type_media,
                "titre": media["titre"],
                "image": media["image"],
                "image_secondaire": media["image_secondaire"],
                "saisons": saisons_a_voir,
            })

    return resultats


# Recherche les films à voir dans toutes les collections.
def rechercher_films_collections():
    media_manager = MediaManager("film")

    films = media_manager.lister_medias()

    resultats = []
    collections_deja_traitees = []

    for film in films:
        collection_id = film["collection_id"]

        if collection_id is None:
            continue

        if collection_id in collections_deja_traitees:
            continue

        collections_deja_traitees.append(collection_id)

        films_tmdb = recuperer_collection(collection_id)

        if films_tmdb is None:
            continue

        films_locaux = [
            film_local["tmdb_id"]
            for film_local in films
            if film_local["collection_id"] == collection_id
        ]

        films_a_voir = comparer_films_collection(
            films_locaux,
            films_tmdb,
        )

        if films_a_voir:
            resultats.append({
                "type": "film",
                "collection": film["collection_nom"],
                "films": films_a_voir,
            })

    return resultats


# Recherche tous les contenus à voir.
def rechercher_a_voir():
    return {
        "series": rechercher_saisons("serie"),
        "animes": rechercher_saisons("anime"),
        "films": rechercher_films_collections(),
    }


# ----------------------------------------------------------------------
# TMDB
# ----------------------------------------------------------------------

# Récupère les films présents dans une collection TMDB.
def recuperer_collection(collection_id):
    from app.common.tmdb import (
        TMDB_API_URL,
        preparer_parametres,
        creer_requete_tmdb,
        executer_requete_tmdb,
    )

    parametres = preparer_parametres({
        "language": "fr-FR",
    })

    url = (
        f"{TMDB_API_URL}/collection/"
        f"{collection_id}?{parametres}"
    )

    requete = creer_requete_tmdb(url)

    try:
        collection = executer_requete_tmdb(requete)

        if not collection:
            return None

        return collection.get("parts", [])

    except urllib.error.HTTPError as error:
        print(f"Erreur HTTP TMDB : {error.code}")
        print(error.read().decode("utf-8"))
        return None

    except urllib.error.URLError as error:
        print("Erreur de connexion à TMDB :")
        print(error.reason)
        return None

    except TimeoutError:
        print("TMDB a mis trop de temps à répondre.")
        return None

    except Exception as erreur:
        print(
            "Erreur récupération collection TMDB :",
            repr(erreur),
        )
        return None


# ----------------------------------------------------------------------
# Formatage
# ----------------------------------------------------------------------

def formater_duree(minutes):
    if not minutes:
        return None

    heures, minutes_restantes = divmod(minutes, 60)

    if heures and minutes_restantes:
        return f"{heures}h{minutes_restantes:02d}"

    if heures:
        return f"{heures}h"

    return f"{minutes_restantes} min"


# ----------------------------------------------------------------------
# Test manuel
# ----------------------------------------------------------------------

if __name__ == "__main__":
    resultats = rechercher_a_voir()

    print("Séries à voir :")

    for serie in resultats["series"]:
        print(
            serie["titre"],
            "→ saisons :",
            serie["saisons"],
        )

    print()
    print("Anime à voir :")

    for anime in resultats["animes"]:
        print(
            anime["titre"],
            "→ saisons :",
            anime["saisons"],
        )

    print()
    print("Films à voir :")

    for collection in resultats["films"]:
        print(
            collection["collection"],
            "→ films :",
        )

        for film in collection["films"]:
            print(
                film["title"],
                "→ TMDB :",
                film["id"],
            )