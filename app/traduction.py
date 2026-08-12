import json
import urllib.parse
import urllib.request


def traduire_anglais_francais(texte):

    params = urllib.parse.urlencode({
        "q": texte,
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

    return resultat["responseData"]["translatedText"]