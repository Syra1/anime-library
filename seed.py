from app.database import (
    create_tables,
    ajouter_anime,
    ajouter_saison,
    get_saison,
    marquer_saison_vue
)


# Créer les tables si elles n'existent pas
create_tables()

print("Base de données initialisée !")


# Données de test
titre = "L'Attaque des Titans"
titre_original = "Shingeki no Kyojin"
statut = "Terminé"
nombre_saisons = 4


# Ajouter l'anime
anime_id = ajouter_anime(
    titre,
    titre_original,
    statut
)


# Ajouter les saisons
for numero in range(1, nombre_saisons + 1):
    ajouter_saison(anime_id, numero)


# Marquer les saisons 1 et 2 comme vues
for numero in [1, 2]:
    saison = get_saison(anime_id, numero)

    if saison:
        marquer_saison_vue(
            anime_id,
            saison["id"]
        )


print(f"Anime ajouté : {titre}")
print(f"Nombre de saisons : {nombre_saisons}")
print("Saisons 1 et 2 marquées comme vues !")
