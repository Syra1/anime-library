// ============================================================
// Suppression du film
// ============================================================

async function handleDeleteFilm(event) {

    const deleteButton = event.currentTarget;

    const filmId = Number(
        deleteButton.dataset.filmId
    );

    try {

        const response = await fetch(
            `/film/films/${filmId}`,
            {
                method: "DELETE"
            }
        );

        if (!response.ok) {

            throw new Error(
                "Erreur lors de la suppression"
            );

        }

        const resultat = await response.json();

        if (!resultat.success) {

            throw new Error(
                "Impossible de supprimer le film"
            );

        }

        window.location.href = "/film/";

    } catch (error) {

        console.error(error);

        alert(
            "Impossible de supprimer le film."
        );

    }
}



// ============================================================
// Initialisation
// ============================================================

const deleteButton = document.querySelector(
    ".delete-film-button"
);

if (deleteButton) {

    deleteButton.addEventListener(
        "click",
        handleDeleteFilm
    );

}