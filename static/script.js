console.log("NOUVEAU SCRIPT 43"); 

let animes = [];

let currentFilter = "all";


// ============================================================
// BIBLIOTHÈQUE
// ============================================================


// Charger les animés depuis notre API FastAPI
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

        document.getElementById(
            "anime-list"
        ).innerHTML = `
            <p>
                Impossible de charger les animés.
            </p>
        `;
    }
}


// Afficher les animés de la bibliothèque
function displayAnimes() {

    const searchInput =
        document.getElementById("search");

    const search =
        searchInput.value.toLowerCase();

    const animeList =
        document.getElementById("anime-list");


    // Filtrer les animés
    const filteredAnimes =
        animes.filter(anime => {

            const matchesSearch =
                anime.titre
                    .toLowerCase()
                    .includes(search)

                ||

                (
                    anime.titre_original &&

                    anime.titre_original
                        .toLowerCase()
                        .includes(search)
                );


            return matchesSearch;

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


    // Afficher les animés
    animeList.innerHTML =
        filteredAnimes
            .map(anime => {

                return `
                    <article
                        class="anime-card"
                    >

                        <h2>
                            ${anime.titre}
                        </h2>

                        <p class="original-title">
                            ${
                                anime.titre_original
                                ||
                                "Titre original inconnu"
                            }
                        </p>

                        <p>
                            Statut :
                            ${anime.statut || "Inconnu"}
                        </p>

                        <button
                            class="delete-anime-button"
                            data-anime-id="${anime.id}"
                        >
                            🗑️ Supprimer
                        </button>



                        <div class="seasons">

                            ${
                                anime.saisons
                                    .map(saison => {

                                        const classe =
                                            saison.vue
                                                ? "watched"
                                                : "unwatched";


                                        return `
                                            <button
                                                class="
                                                    season-button
                                                    ${classe}
                                                "
                                                data-anime-id="
                                                    ${anime.id}
                                                "
                                                data-season-id="
                                                    ${saison.id}
                                                "
                                                data-season-number="
                                                    ${saison.numero}
                                                "
                                            >
                                                Saison
                                                ${saison.numero}
                                            </button>
                                        `;

                                    })
                                    .join("")
                            }

                        </div>

                    </article>
                `;

            })
            .join("");


    // Ajouter les événements
    // sur les boutons de saison
    document
        .querySelectorAll(".season-button")
        .forEach(button => {

            button.addEventListener(
                "click",
                handleSeasonClick
            );

        });

    document
    .querySelectorAll(".delete-anime-button")
    .forEach(button => {

        button.addEventListener(
            "click",
            handleDeleteAnime
        );

    });

}


// Gestion du clic sur une saison
async function handleSeasonClick(event) {

    const button =
        event.currentTarget;


    const animeId =
        Number(
            button.dataset.animeId
        );


    const seasonNumber =
        Number(
            button.dataset.seasonNumber
        );


    // Récupérer l'anime concerné
    const anime =
        animes.find(
            anime =>
                anime.id === animeId
        );


    if (!anime) {
        return;
    }


    // Déterminer uniquement les saisons
    // dont l'état change.
    const changements = [];

    anime.saisons.forEach(saison => {

        const nouvelleValeur =
            saison.numero <= seasonNumber;

        if (saison.vue !== nouvelleValeur) {

            changements.push({
                id: saison.id,
                vue: nouvelleValeur
            });

            // Mise à jour locale
            saison.vue = nouvelleValeur;

        }

    });


    // Rien n'a changé
    if (changements.length === 0) {

        return;

    }


    try {

        const response =
            await fetch(
                "/animes/"
                + animeId
                + "/saisons",
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

            throw new Error(
                "Erreur lors de la mise à jour"
            );

        }


        displayAnimes();

    } catch (error) {

        console.error(error);

        alert(
            "Impossible de mettre à jour la saison."
        );

    }

}


async function handleDeleteAnime(event) {

    const animeId =
        Number(
            event.currentTarget.dataset.animeId
        );

    if (
        !confirm(
            "Supprimer cet anime de la bibliothèque ?"
        )
    ) {
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
            throw new Error();
        }


        loadAnimes();

    } catch(error) {

        console.error(error);

        alert(
            "Impossible de supprimer l'anime."
        );

    }

}


// Recherche dans la bibliothèque
document
    .getElementById("search")
    .addEventListener(
        "input",
        displayAnimes
    );


// ============================================================
// RECHERCHE ANILIST
// ============================================================


const animeSearch =
    document.getElementById(
        "anime-search"
    );


const searchResults =
    document.getElementById(
        "search-results"
    );


// Attendre un petit moment avant
// d'envoyer la requête à AniList
let searchTimeout = null;


animeSearch.addEventListener(
    "input",
    () => {

        const recherche =
            animeSearch.value.trim();


        // Annuler la recherche précédente
        clearTimeout(
            searchTimeout
        );


        // Si moins de 3 caractères
        // on ne recherche rien
        if (recherche.length < 3) {

            searchResults.innerHTML = "";

            return;
        }


        // Attendre 500 ms après
        // la dernière frappe
        searchTimeout =
            setTimeout(
                () => {

                    searchAniList(
                        recherche
                    );

                },
                500
            );

    }
);


// Rechercher un anime sur AniList
async function searchAniList(
    recherche
) {

    searchResults.innerHTML = `
        <p>
            Recherche en cours...
        </p>
    `;


    try {

        const response =
            await fetch(
                "/search-anime?q="
                +
                encodeURIComponent(
                    recherche
                )
            );


        if (!response.ok) {

            throw new Error(
                "Erreur lors de la recherche"
            );

        }


        const resultats =
            await response.json();


        displaySearchResults(
            resultats
        );


    } catch (error) {

        console.error(error);

        searchResults.innerHTML = `
            <p>
                Impossible de rechercher
                cet anime.
            </p>
        `;

    }

}


// Afficher les résultats AniList
function displaySearchResults(resultats) {

    if (
        !resultats ||
        resultats.length === 0
    ) {

        searchResults.innerHTML = `
            <p>
                Aucun anime trouvé.
            </p>
        `;

        return;
    }


    searchResults.innerHTML = `
        <div class="search-results-list">

            ${
                resultats
                    .map(anime => {

                        const titrePrincipal =
                            anime.title.english
                            ||
                            anime.title.romaji
                            ||
                            anime.title.native;


                        const titreSecondaire =
                            anime.title.romaji
                            ||
                            anime.title.native;


                        return `
                            <article
                                class="search-result"
                            >

                                <div
                                    class="search-result-info"
                                >

                                    <h3>
                                        ${titrePrincipal}
                                    </h3>

                                    <p>
                                        ${titreSecondaire}
                                    </p>

                                    <small>
                                        Statut :
                                        ${anime.status}
                                    </small>

                                </div>


                                <button
                                    class="add-anime-button"
                                    data-anilist-id="
                                        ${anime.id}
                                    "
                                >
                                    Ajouter
                                </button>

                            </article>
                        `;

                    })
                    .join("")
            }

        </div>
    `;


    // Ajouter l'événement
    // aux boutons "Ajouter"
    document
        .querySelectorAll(
            ".add-anime-button"
        )
        .forEach(button => {

            button.addEventListener(
                "click",
                handleAddAnime
            );

        });

}

// Ajouter un anime à la bibliothèque
async function handleAddAnime(event) {

    const button =
        event.currentTarget;


    const anilistId =
        Number(
            button.dataset.anilistId
        );


    try {

        const response =
            await fetch(
                "/add-anime/"
                + anilistId,
                {
                    method: "POST"
                }
            );


        const resultat =
            await response.json();


        if (!resultat.success) {

            throw new Error(
                "Ajout impossible"
            );

        }


        alert(
            "Anime ajouté à la bibliothèque !"
        );


        loadAnimes();


    } catch(error) {

        console.error(error);

        alert(
            "Erreur pendant l'ajout."
        );

    }

}


// ============================================================
// INITIALISATION
// ============================================================


// Charger la bibliothèque
// au chargement de la page
loadAnimes();
