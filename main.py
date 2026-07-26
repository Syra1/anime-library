from app.database import create_tables, ajouter_anime, lister_animes


create_tables()

print("Base de données initialisée !")

animes = lister_animes()

print("Liste des animés :")

for anime in animes:
        print(anime)
