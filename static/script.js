let animes = [];


async function loadAnimes() {

    try {

        const response = await fetch("/animes");

        if (!response.ok) {
            throw new Error(
                "Erreur lors du chargement des animés"
            );
        }

        animes = await response.json();

        displayAnimes();

    } catch (error) {

        console.error(error);

        document.getElementById("anime-list").innerHTML = `
            <p>
                Impossible de charger les animés.
            </p>
        `;

    }

}


function displayAnimes() {

    const searchInput =
        document.getElementById("search");

    const search =
        searchInput.value.toLowerCase();

    const animeList =
        document.getElementById("anime-list");


    // Filtrer les animés selon la recherche
    const filteredAnimes =
        animes.filter(anime => {

            return (
                anime.titre
                    .toLowerCase()
                    .includes(search)
                ||
                (
                    anime.titre_original
                    &&
                    anime.titre_original
                        .toLowerCase()
                        .includes(search)
                )
            );

        });


    // Aucun résultat
    if (filteredAnimes.length === 0) {

        animeList.innerHTML = `
            <p>
                Aucun anime trouvé.
            </p>
        `;

        return;

    }


    // Construire le HTML des animés
    animeList.innerHTML =
        filteredAnimes
            .map(anime => {


                // Compter les saisons vues
                const saisonsVues =
                    anime.saisons.filter(
                        saison => saison.vue
                    ).length;


                // Nombre total de saisons
                const nombreSaisons =
                    anime.saisons.length;


                // Construire le HTML des saisons
                const saisonsHTML =
                    anime.saisons
                        .map(saison => {

                            const symbole =
                                saison.vue
                                    ? "✓"
                                    : "○";


                            const classe =
                                saison.vue
                                    ? "season watched"
                                    : "season unwatched";


                            return `
                                <button
                                    class="${classe}"
                                    data-anime-id="${anime.id}"
                                    data-saison-id="${saison.id}"
                                    data-vue="${saison.vue}"
                                >
                                    ${symbole}
                                    Saison ${saison.numero}
                                </button>
                            `;

                        })
                        .join("");


                // Retourner la carte complète de l'anime
                return `
                    <article class="anime-card">

                        <h2>
                            ${anime.titre}
                        </h2>

                        <p class="original-title">
                            ${anime.titre_original || ""}
                        </p>

                        <p class="anime-status">
                            Statut :
                            ${anime.statut || "Inconnu"}
                        </p>

                        <h3>
                            Saisons
                        </h3>

                        <div class="season-list">
                            ${saisonsHTML}
                        </div>

                        <p class="progression">
                            ${saisonsVues}
                            /
                            ${nombreSaisons}
                            saisons vues
                        </p>

                    </article>
                `;

            })
            .join("");


    // Récupérer tous les boutons de saison
    const boutonsSaison =
        document.querySelectorAll(".season");


    // Ajouter un événement à chaque bouton
    boutonsSaison.forEach(button => {

        button.addEventListener(
            "click",
            modifierSaison
        );

    });

}

async function modifierSaison(event) {

    const button =
        event.currentTarget;

    const animeId =
        Number(button.dataset.animeId);

    const saisonId =
        Number(button.dataset.saisonId);


    // Trouver l'anime concerné
    const anime =
        animes.find(
            anime => anime.id === animeId
        );


    if (!anime) {
        return;
    }


    // Trouver la saison cliquée
    const saisonCliquee =
        anime.saisons.find(
            saison => saison.id === saisonId
        );


    if (!saisonCliquee) {
        return;
    }


    // La saison cliquée devient la dernière
    // saison regardée
    const derniereSaisonVue =
        saisonCliquee.numero;


    try {

        // Parcourir toutes les saisons
        for (const saison of anime.saisons) {

            // Toutes les saisons jusqu'à
            // la saison cliquée sont vues
            const nouvelleVue =
                saison.numero <= derniereSaisonVue;


            const response = await fetch(
                `/animes/${animeId}/saisons/${saison.id}?vue=${nouvelleVue}`,
                {
                    method: "PUT"
                }
            );


            if (!response.ok) {

                throw new Error(
                    "Impossible de modifier la saison"
                );

            }

        }


        // Recharger les données depuis SQLite
        await loadAnimes();


    } catch (error) {

        console.error(error);

        alert(
            "Impossible de modifier les saisons."
        );

    }

}

// Rechercher un anime
document
    .getElementById("search")
    .addEventListener(
        "input",
        displayAnimes
    );


// Charger les animés au démarrage
loadAnimes();
