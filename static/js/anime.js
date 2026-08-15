// Gère la sélection d'une saison et met à jour les saisons vues.
async function handleSeasonClick(event) {
    const button = event.currentTarget;
    const animeId = Number(button.dataset.animeId);
    const seasonNumber = Number(button.dataset.seasonNumber);
    const boutons = document.querySelectorAll(".season-button");
    const changements = [];
    boutons.forEach(btn => {
        const numero = Number(btn.dataset.seasonNumber);
        changements.push({
            id: Number(btn.dataset.seasonId),
            vue: numero <= seasonNumber
        });
    });
    await fetch("/animes/" + animeId + "/saisons", {
        method: "PUT", headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
                saisons: changements
        })
    });
    location.reload();
}

document.querySelectorAll(".season-button").forEach(button => {
    button.addEventListener("click", handleSeasonClick);
});


// Supprime l'anime sélectionné et revient à la bibliothèque.
async function handleDeleteAnime(event) {
    const deleteButton = event.currentTarget;
    const animeId = Number(deleteButton.dataset.animeId);
    try {
        const response = await fetch("/animes/" + animeId, {
            method: "DELETE"
        });
        if (!response.ok) {
            throw new Error("Erreur suppression");
        }
        window.location.href = "/";
    } catch (error) {
        console.error(error);
        alert("Impossible de supprimer l'anime.");
    }
}

const deleteButton = document.querySelector(".delete-anime-button");

if (deleteButton) {
    deleteButton.addEventListener("click", handleDeleteAnime);
}

// 
document.addEventListener("DOMContentLoaded", () => {

    const controls = document.querySelector(".season-controls");
    if (!controls) return;

    const animeId = controls.dataset.animeId;

    const addBtn = controls.querySelector(".add-season-btn");
    const removeBtn = controls.querySelector(".remove-season-btn");

    addBtn.addEventListener("click", async () => {
        const response = await fetch(
            `/animes/${animeId}/saisons/ajouter`,
            { method: "POST" }
        );

        const resultat = await response.json();

        if (resultat.success) {
            window.location.reload();
        }
    });

    removeBtn.addEventListener("click", async () => {

        const response = await fetch(
            `/animes/${animeId}/saisons/retirer`,
            { method: "DELETE" }
        );

        const resultat = await response.json();

        if (resultat.success) {
            window.location.reload();
        }
    });

});