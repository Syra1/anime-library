from app.common.tmdb import recuperer_collection
from app.common.database import (
    execute_query,
    fetch_all,
    fetch_one,
    modifier_saison_vue as modifier_saison_vue_database,
)


# Configuration des différents types de médias.
#
# "colonnes" liste les champs stockés en base pour ce type de média,
# dans l'ordre utilisé pour les INSERT. Elle sert aussi de référence
# unique pour éviter de répéter la liste des colonnes à chaque requête.
MEDIA_CONFIG = {
    "film": {
        "table": "film",
        "avec_saisons": False,
        "colonnes": [
            "tmdb_id", "titre", "titre_original", "image", "image_secondaire",
            "description", "annee", "genres", "duree", "auteur", "realisateur",
            "collection_id", "collection_nom",
        ],
    },
    "serie": {
        "table": "serie",
        "table_saison": "saison_serie",
        "id_saison": "serie_id",
        "avec_saisons": True,
        "colonnes": [
            "tmdb_id", "titre", "titre_original", "image", "image_secondaire",
            "description", "annee", "genres", "duree", "auteur",
            "realisateur", "nombre_saisons",
        ],
    },
    "anime": {
        "table": "anime",
        "table_saison": "saison_anime",
        "id_saison": "anime_id",
        "avec_saisons": True,
        "colonnes": [
            "tmdb_id", "titre", "titre_original", "image", "image_secondaire",
            "description", "annee", "genres", "duree", "auteur",
            "realisateur", "nombre_saisons",
        ],
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
        table = self.config["table"]
        colonnes = self.config["colonnes"]

        placeholders = ", ".join("?" for _ in colonnes)
        valeurs = tuple(donnees.get(colonne) for colonne in colonnes)

        cursor = execute_query(
            f"""
            INSERT INTO {table} ({', '.join(colonnes)})
            VALUES ({placeholders})
            """,
            valeurs,
        )

        media_id = cursor.lastrowid

        if self.config["avec_saisons"]:
            self._ajouter_saisons(media_id, donnees.get("saisons", []))

        return media_id

    def _ajouter_saisons(self, media_id, saisons):
        table_saison = self.config["table_saison"]
        id_saison = self.config["id_saison"]

        for saison in saisons:
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

    # ------------------------------------------------------------------
    # Liste des médias
    # ------------------------------------------------------------------

    def lister_medias(self, avec_saisons=False):
        table = self.config["table"]

        if self.type_media == "film":
            return self._lister_films(table)

        return self._lister_medias_avec_saisons(table, avec_saisons)

    def _lister_films(self, table):
        films = fetch_all(
            f"""
            SELECT *
            FROM {table}
            ORDER BY
                COALESCE(collection_nom, titre) COLLATE NOCASE ASC,
                annee ASC,
                titre COLLATE NOCASE ASC
            """
        )

        suivis = self._creer_suivis_collections(films)

        return [
            {**dict(film), "suivi": suivis.get(film["collection_id"])}
            for film in films
        ]

    def _lister_medias_avec_saisons(self, table, avec_saisons):
        medias = fetch_all(
            f"""
            SELECT *
            FROM {table}
            ORDER BY titre COLLATE NOCASE ASC, annee ASC
            """
        )

        if not avec_saisons:
            return [
                {
                    **dict(media),
                    "suivi": creer_suivi_media(
                        self.compter_saisons_vues(media["id"]),
                        media["nombre_saisons"],
                    ),
                }
                for media in medias
            ]

        saisons_par_media = self._lister_saisons_par_media(
            [media["id"] for media in medias]
        )

        resultats = []

        for media in medias:
            saisons = saisons_par_media.get(media["id"], [])

            resultats.append({
                **dict(media),
                "saisons": saisons,
                "suivi": creer_suivi_media(
                    sum(saison["vu"] for saison in saisons),
                    media["nombre_saisons"],
                ),
            })

        return resultats

    # Récupère les saisons de plusieurs médias en une seule requête,
    # regroupées par média (évite une requête par média).
    def _lister_saisons_par_media(self, medias_ids):
        if not medias_ids:
            return {}

        table_saison = self.config["table_saison"]
        id_saison = self.config["id_saison"]
        placeholders = ", ".join("?" for _ in medias_ids)

        saisons = fetch_all(
            f"""
            SELECT
                {id_saison} AS media_id,
                id,
                titre,
                numero,
                nombre_episodes,
                vu
            FROM {table_saison}
            WHERE {id_saison} IN ({placeholders})
            ORDER BY numero ASC
            """,
            tuple(medias_ids),
        )

        saisons_par_media = {}

        for saison in saisons:
            saisons_par_media.setdefault(saison["media_id"], []).append({
                "id": saison["id"],
                "titre": saison["titre"],
                "numero": saison["numero"],
                "nombre_episodes": saison["nombre_episodes"],
                "vu": saison["vu"],
            })

        return saisons_par_media

    def _creer_suivis_collections(self, films):
        suivis = {}
        collections_deja_traitees = set()

        for film in films:
            collection_id = film["collection_id"]

            if collection_id is None or collection_id in collections_deja_traitees:
                continue

            collections_deja_traitees.add(collection_id)

            films_tmdb = recuperer_collection(collection_id)

            if films_tmdb is None:
                continue

            nb_films_locaux = sum(
                1 for film_local in films
                if film_local["collection_id"] == collection_id
            )

            suivis[collection_id] = creer_suivi_media(nb_films_locaux, len(films_tmdb))

        return suivis

    # ------------------------------------------------------------------
    # Récupération d'un média
    # ------------------------------------------------------------------

    def recuperer_media(self, media_id):
        table = self.config["table"]

        media = fetch_one(
            f"SELECT * FROM {table} WHERE id = ?",
            (media_id,),
        )

        if media is None:
            return None

        resultat = dict(media)

        if self.config["avec_saisons"]:
            resultat["saisons"] = self._lister_saisons(media_id)

        return resultat

    def _lister_saisons(self, media_id):
        table_saison = self.config["table_saison"]
        id_saison = self.config["id_saison"]

        saisons = fetch_all(
            f"""
            SELECT id, titre, numero, nombre_episodes, vu
            FROM {table_saison}
            WHERE {id_saison} = ?
            ORDER BY numero ASC
            """,
            (media_id,),
        )

        return [dict(saison) for saison in saisons]

    # ------------------------------------------------------------------
    # Suppression
    # ------------------------------------------------------------------

    def supprimer_media(self, media_id):
        table = self.config["table"]

        execute_query(
            f"DELETE FROM {table} WHERE id = ?",
            (media_id,),
        )

    # ------------------------------------------------------------------
    # Gestion des saisons
    # ------------------------------------------------------------------

    def _verifier_avec_saisons(self):
        if not self.config["avec_saisons"]:
            raise ValueError(
                f"Le média '{self.type_media}' ne possède pas de saisons."
            )

    def compter_saisons_vues(self, media_id):
        self._verifier_avec_saisons()

        table_saison = self.config["table_saison"]
        id_saison = self.config["id_saison"]

        saisons = fetch_all(
            f"SELECT vu FROM {table_saison} WHERE {id_saison} = ?",
            (media_id,),
        )

        return sum(saison["vu"] for saison in saisons)

    def modifier_saison_vue(self, saisons_ids, vu):
        self._verifier_avec_saisons()

        modifier_saison_vue_database(
            self.type_media,
            saisons_ids,
            vu,
        )


def creer_suivi_media(vus, total):
    return {
        "vus": vus,
        "total": total,
    }