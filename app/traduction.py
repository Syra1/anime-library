import json
import urllib.parse
import urllib.request


def traduire_anglais_francais(texte):

    if not texte:
        return ""

    morceaux = []

    for paragraphe in texte.split("\n\n"):

        while len(paragraphe) > 500:
            morceaux.append(paragraphe[:500])
            paragraphe = paragraphe[500:]

        morceaux.append(paragraphe)

    traductions = []

    for morceau in morceaux:

        params = urllib.parse.urlencode({
            "q": morceau,
            "langpair": "en|fr"
        })

        url = (
            "https://api.mymemory.translated.net/get?"
            + params
        )

        with urllib.request.urlopen(url) as response:

            resultat = json.loads(
                response.read().decode("utf-8")
            )

        traductions.append(
            resultat["responseData"]["translatedText"]
        )

    return "\n\n".join(traductions)