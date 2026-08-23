// ============================================================
// Sélection d'une saison
// ============================================================

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

    try {
        const response = await fetch(
            `/anime/animes/${animeId}/saisons`,
            {
                method: "PUT",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({
                    saisons: changements
                })
            }
        );

        if (!response.ok) {
            throw new Error("Erreur lors de la mise à jour des saisons");
        }

        // Mise à jour visuelle immédiate
        boutons.forEach(btn => {
            const numero = Number(btn.dataset.seasonNumber);
            const vue = numero <= seasonNumber;

            btn.classList.toggle("watched", vue);
            btn.classList.toggle("unwatched", !vue);
        });

    } catch (error) {
        console.error(error);
        alert("Impossible de mettre à jour les saisons.");
    }
}


// ============================================================
// Suppression de l'anime
// ============================================================

async function handleDeleteAnime(event) {
    const deleteButton = event.currentTarget;
    const animeId = Number(deleteButton.dataset.animeId);

    try {
        const response = await fetch(
            `/anime/animes/${animeId}`,
            {
                method: "DELETE"
            }
        );

        if (!response.ok) {
            throw new Error("Erreur lors de la suppression");
        }

        window.location.href = "/anime/";

    } catch (error) {
        console.error(error);
        alert("Impossible de supprimer l'anime.");
    }
}


// ============================================================
// Ajout d'une saison
// ============================================================

async function handleAddSeason(animeId) {
    try {
        const response = await fetch(
            `/anime/animes/${animeId}/saisons/ajouter`,
            {
                method: "POST"
            }
        );

        if (!response.ok) {
            throw new Error("Erreur lors de l'ajout de la saison");
        }

        const resultat = await response.json();

        if (!resultat.success) {
            throw new Error("Impossible d'ajouter la saison");
        }

        ajouterBoutonSaison(
            resultat.saison,
            animeId
        );

    } catch (error) {
        console.error(error);
        alert("Impossible d'ajouter la saison.");
    }
}


// ============================================================
// Création du bouton d'une nouvelle saison
// ============================================================

function ajouterBoutonSaison(saison, animeId) {
    const seasonsContainer = document.querySelector(".seasons");

    if (!seasonsContainer) {
        return;
    }

    const button = document.createElement("button");

    button.type = "button";
    button.className = saison.vue
        ? "season-button watched"
        : "season-button unwatched";

    button.dataset.animeId = animeId;
    button.dataset.seasonId = saison.id;
    button.dataset.seasonNumber = saison.numero;

    button.textContent = `Saison ${saison.numero}`;

    button.addEventListener(
        "click",
        handleSeasonClick
    );

    seasonsContainer.appendChild(button);
}


// ============================================================
// Suppression de la dernière saison
// ============================================================

async function handleRemoveSeason(animeId) {
    try {
        const response = await fetch(
            `/anime/animes/${animeId}/saisons/retirer`,
            {
                method: "DELETE"
            }
        );

        if (!response.ok) {
            throw new Error("Erreur lors de la suppression de la saison");
        }

        const resultat = await response.json();

        if (!resultat.success) {
            throw new Error("Impossible de supprimer la saison");
        }

        supprimerDernierBoutonSaison();

    } catch (error) {
        console.error(error);
        alert("Impossible de supprimer la saison.");
    }
}


// ============================================================
// Suppression visuelle du dernier bouton
// ============================================================

function supprimerDernierBoutonSaison() {
    const seasonsContainer = document.querySelector(".seasons");

    if (!seasonsContainer) {
        return;
    }

    const boutons = seasonsContainer.querySelectorAll(
        ".season-button"
    );

    if (boutons.length === 0) {
        return;
    }

    boutons[boutons.length - 1].remove();
}


// ============================================================
// Initialisation
// ============================================================

function initializeSeasonControls() {
    const controls = document.querySelector(".season-controls");

    if (!controls) {
        return;
    }

    const animeId = controls.dataset.animeId;

    const addButton = controls.querySelector(
        ".add-season-btn"
    );

    const removeButton = controls.querySelector(
        ".remove-season-btn"
    );

    if (addButton) {
        addButton.addEventListener(
            "click",
            () => handleAddSeason(animeId)
        );
    }

    if (removeButton) {
        removeButton.addEventListener(
            "click",
            () => handleRemoveSeason(animeId)
        );
    }
}


// ============================================================
// Événements
// ============================================================

document.querySelectorAll(
    ".season-button"
).forEach(button => {

    button.addEventListener(
        "click",
        handleSeasonClick
    );

});


const deleteButton = document.querySelector(
    ".delete-anime-button"
);

if (deleteButton) {
    deleteButton.addEventListener(
        "click",
        handleDeleteAnime
    );
}


document.addEventListener(
    "DOMContentLoaded",
    initializeSeasonControls
);