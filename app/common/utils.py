def convertir_liste_en_texte(elements):
    if not elements:
        return ""

    return ", ".join(
        str(element)
        for element in elements
    )


def formater_duree(minutes):
    if not minutes:
        return None

    heures, minutes_restantes = divmod(minutes, 60)

    if heures and minutes_restantes:
        return f"{heures}h{minutes_restantes:02d}"

    if heures:
        return f"{heures}h"

    return f"{minutes_restantes} min"


def determiner_type_media(media):
    genre_ids = media.get("genre_ids", [])

    if 16 in genre_ids:
        return "anime"

    return "serie"