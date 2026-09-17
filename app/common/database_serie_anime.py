
from app.common.database import (
    get_connection,
    execute_query,
    fetch_all,
    fetch_one,
    modifier_saison_vue,
    creer_suivi_media,
)


# ============================================================
# CONFIGURATION DES TYPES DE MÉDIAS
# ============================================================

MEDIA_CONFIG = {
    "serie": {
        "table": "serie",
        "table_saison": "saison_serie",
        "id_saison": "serie_id",
    },
    "anime": {
        "table": "anime",
        "table_saison": "saison_anime",
        "id_saison": "anime_id",
    },
}


def _get_config(type_media):
    """
    Retourne la configuration correspondant au type de média.
    """
    if type_media not in MEDIA_CONFIG:
        raise ValueError(
            f"Type de média invalide : {type_media}. "
            f"Valeurs acceptées : {', '.join(MEDIA_CONFIG.keys())}"
        )

    return MEDIA_CONFIG[type_media]


# ============================================================
# MODIFICATION DU STATUT DES SAISONS
# ============================================================

def modifier_saison_vue(type_media, saisons_ids, vu):
    """
    Modifie le statut vu/non vu des saisons d'un média.

    type_media : "serie" ou "anime"
    saisons_ids : liste des IDs des saisons
    vu : 0 ou 1
    """
    _get_config(type_media)

    modifier_saison_vue(type_media, saisons_ids, vu)


# Alias conservés pour compatibilité avec l'ancien code
def modifier_saison_vue_serie(saisons_ids, vu):
    modifier_saison_vue("serie", saisons_ids, vu)


def modifier_saison_vue_anime(saisons_ids, vu):
    modifier_saison_vue("anime", saisons_ids, vu)


# ============================================================
# CRÉATION DES TABLES
# ============================================================

def create_tables():
    connection = get_connection()

    # --------------------------------------------------------
    # Table série
    # --------------------------------------------------------

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

    connection.execute(
        """
        CREATE TABLE IF NOT EXISTS saison_serie (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            serie_id INTEGER NOT NULL,
            titre TEXT,
            numero INTEGER NOT NULL,
            nombre_episodes INTEGER NOT NULL,
            vu INTEGER NOT NULL DEFAULT 0,
            FOREIGN KEY (serie_id) REFERENCES serie(id) ON DELETE CASCADE
        )
        """
    )

    # --------------------------------------------------------
    # Table anime
    # --------------------------------------------------------

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

    connection.execute(
        """
        CREATE TABLE IF NOT EXISTS saison_anime (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            anime_id INTEGER NOT NULL,
            titre TEXT,
            numero INTEGER NOT NULL,
            nombre_episodes INTEGER NOT NULL,
            vu INTEGER NOT NULL DEFAULT 0,
            FOREIGN KEY (anime_id) REFERENCES anime(id) ON DELETE CASCADE
        )
        """
    )

    connection.commit()
    connection.close()


# ============================================================
# AJOUT D'UN MÉDIA
# ============================================================

def ajouter_media(
    type_media,
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
    nombre_saisons,
    saisons,
):
    config = _get_config(type_media)

    table = config["table"]
    table_saison = config["table_saison"]
    id_saison = config["id_saison"]

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
            nombre_saisons,
        ),
    )

    media_id = cursor.lastrowid

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

    return media_id


# Alias conservés pour compatibilité avec l'ancien code
def ajouter_serie(
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
    nombre_saisons,
    saisons,
):
    return ajouter_media(
        "serie",
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
        nombre_saisons,
        saisons,
    )


def ajouter_anime(
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
    nombre_saisons,
    saisons,
):
    return ajouter_media(
        "anime",
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
        nombre_saisons,
        saisons,
    )


# ============================================================
# LISTE DES MÉDIAS
# ============================================================

def lister_medias(type_media):
    config = _get_config(type_media)

    table = config["table"]

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
        ORDER BY {table}.titre COLLATE NOCASE ASC, {table}.annee ASC
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
                compter_saisons_vues(type_media, media["id"]),
                media["nombre_saisons"],
            ),
        }
        for media in medias
    ]


# Alias conservés pour compatibilité avec l'ancien code
def lister_series():
    return lister_medias("serie")


def lister_animes():
    return lister_medias("anime")


# ============================================================
# SUPPRESSION D'UN MÉDIA
# ============================================================

def supprimer_media(type_media, media_id):
    config = _get_config(type_media)

    table = config["table"]

    execute_query(
        f"""
        DELETE FROM {table}
        WHERE id = ?
        """,
        (media_id,),
    )


# Alias conservés pour compatibilité avec l'ancien code
def supprimer_serie(serie_id):
    supprimer_media("serie", serie_id)


def supprimer_anime(anime_id):
    supprimer_media("anime", anime_id)


# ============================================================
# RÉCUPÉRATION D'UN MÉDIA
# ============================================================

def recuperer_media(type_media, media_id):
    config = _get_config(type_media)

    table = config["table"]
    table_saison = config["table_saison"]
    id_saison = config["id_saison"]

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


# Alias conservés pour compatibilité avec l'ancien code
def recuperer_serie(serie_id):
    return recuperer_media("serie", serie_id)


def recuperer_anime(anime_id):
    return recuperer_media("anime", anime_id)


# ============================================================
# COMPTAGE DES SAISONS VUES
# ============================================================

def compter_saisons_vues(type_media, media_id):
    config = _get_config(type_media)

    table_saison = config["table_saison"]
    id_saison = config["id_saison"]

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