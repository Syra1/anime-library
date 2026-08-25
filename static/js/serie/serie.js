// ============================================================
// Suppression de la série
// ============================================================

async function handleDeleteSerie(event) {

    const deleteButton =
        event.currentTarget;

    const serieId =
        Number(
            deleteButton.dataset.serieId
        );

    if (!serieId) {
        return;
    }

    try {

        const response =
            await fetch(
                `/serie/series/${serieId}`,
                {
                    method: "DELETE"
                }
            );

        if (!response.ok) {

            throw new Error(
                "Erreur lors de la suppression"
            );

        }

        const resultat =
            await response.json();

        if (!resultat.success) {

            throw new Error(
                "Impossible de supprimer la série"
            );

        }

        window.location.href =
            "/serie/";

    } catch (error) {

        console.error(error);

        alert(
            "Impossible de supprimer la série."
        );

    }
}


// ============================================================
// Initialisation
// ============================================================

const deleteButton =
    document.querySelector(
        ".delete-serie-button"
    );

if (deleteButton) {

    deleteButton.addEventListener(
        "click",
        handleDeleteSerie
    );

}