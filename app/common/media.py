from app.common.tmdb import recuperer_collection
from app.common.database import (
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
    },
    "serie": {
        "table": "serie",
        "table_saison": "saison_serie",
        "id_saison": "serie_id",
        "avec_saisons": True,
    },
    "anime": {
        "table": "anime",
        "table_saison": "saison_anime",
        "id_saison": "anime_id",
        "avec_saisons": True,
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