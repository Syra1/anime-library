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


            const confirmation =
                confirm(
                    "Voulez-vous supprimer cet anime ?"
                );


            if (!confirmation) {
                return;
            }


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
