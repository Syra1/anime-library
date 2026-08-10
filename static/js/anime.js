document
.querySelectorAll(".season-button")
.forEach(button => {

    button.addEventListener(
        "click",
        async () => {

            const animeId =
                Number(
                    button.dataset.animeId
                );

            const seasonNumber =
                Number(
                    button.dataset.seasonNumber
                );


            const boutons =
                document.querySelectorAll(
                    ".season-button"
                );


            const changements = [];


            boutons.forEach(btn => {

                const numero =
                    Number(
                        btn.dataset.seasonNumber
                    );


                changements.push({

                    id:
                        Number(
                            btn.dataset.seasonId
                        ),

                    vue:
                        numero <= seasonNumber

                });

            });


            await fetch(
                "/animes/"
                + animeId
                + "/saisons",
                {

                    method: "PUT",

                    headers: {
                        "Content-Type":
                        "application/json"
                    },

                    body:
                        JSON.stringify({
                            saisons: changements
                        })

                }
            );


            location.reload();

        }
    );

});


// SUPPRESSION ANIME

const deleteButton =
    document.querySelector(
        ".delete-anime-button"
    );


if (deleteButton) {

    deleteButton.addEventListener(
        "click",
        async () => {

            const animeId =
                Number(
                    deleteButton.dataset.animeId
                );

            try {

                const response =
                    await fetch(
                        "/animes/" + animeId,
                        {
                            method: "DELETE"
                        }
                    );


                if (!response.ok) {

                    throw new Error(
                        "Erreur suppression"
                    );

                }


                window.location.href = "/";


            } catch(error) {

                console.error(error);

                alert(
                    "Impossible de supprimer l'anime."
                );

            }

        }
    );

}


document.addEventListener(
    "DOMContentLoaded",
    () => {

        const bouton =
            document.querySelector(
                ".add-season-button"
            );

        if (!bouton) {
            return;
        }

        bouton.addEventListener(
            "click",
            async () => {

                const animeId =
                    bouton.dataset.animeId;

                const response =
                    await fetch(
                        `/animes/${animeId}/saisons/ajouter`,
                        {
                            method: "POST"
                        }
                    );

                const resultat =
                    await response.json();

                if (!resultat.success) {
                    return;
                }

                window.location.reload();
            }
        );
    }
);

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