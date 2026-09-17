import urllib.error

def gerer_erreur(erreur, contexte="", valeur_defaut=None):
    if isinstance(erreur, urllib.error.HTTPError):
        print(f"Erreur HTTP TMDB : {erreur.code}")

        try:
            print(erreur.read().decode("utf-8"))
        except Exception:
            pass

    elif isinstance(erreur, urllib.error.URLError):
        print("Erreur de connexion à TMDB :")
        print(erreur.reason)

    elif isinstance(erreur, TimeoutError):
        print("TMDB a mis trop de temps à répondre.")

    else:
        if contexte:
            print(f"Erreur {contexte} :", repr(erreur))
        else:
            print("Erreur :", repr(erreur))

    return valeur_defaut