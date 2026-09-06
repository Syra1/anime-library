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