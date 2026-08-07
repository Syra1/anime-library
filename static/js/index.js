console.log("NOUVEAU SCRIPT 43");

let animes = [];

const addModal =
    document.getElementById("add-modal");

const seasonCountInput =
    document.getElementById("season-count");


const cancelAddButton =
    document.getElementById("cancel-add");

const confirmAddButton =
    document.getElementById("confirm-add");


let currentAnimeToAdd = null;

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

function normalizeText(text) {

    return (text || "")
        .normalize("NFD")
        .replace(/[\u0300-\u036f]/g, "")
        .toLowerCase();

}

function displayAnimes(search = "") {

    search = normalizeText(search);

    const animeList =
        document.getElementById("anime-list");


    // Filtrer les animés
    const filteredAnimes =
        animes.filter(anime => {

            const matchesSearch =
                normalizeText(anime.titre)
                    .includes(search)

                ||

                (
                    anime.titre_original &&

                    normalizeText(anime.titre_original)
                        .includes(search)
                );

            return matchesSearch;

        });


    if (filteredAnimes.length === 0) {

        animeList.innerHTML = `
            <p>
                Aucun anime trouvé.
            </p>
        `;

        return;
    }


    animeList.innerHTML =
        filteredAnimes
            .map(anime => {

                return `
                    <article class="anime-card">


                        <div class="anime-info">

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

                        </div>

                        <div class="anime-image">

                            <a href="/anime/${anime.id}">
                                <img
                                    src="${anime.image}"
                                    alt="${anime.titre}"
                                >
                            </a>

                        </div>

                    </article>
                `;

            })
            .join("");

}


let librarySearchTimeout = null;


document
    .getElementById("search")
    .addEventListener(
        "input",
        () => {

            clearTimeout(librarySearchTimeout);


            const recherche =
                document
                    .getElementById("search")
                    .value
                    .trim();


            if (recherche.length < 3) {

                displayAnimes("");

                return;
            }


            librarySearchTimeout =
                setTimeout(
                    () => {

                        displayAnimes(recherche);

                    },
                    500
                );

        }
    );


const animeSearch =
    document.getElementById(
        "anime-search"
    );


const searchResults =
    document.getElementById(
        "search-results"
    );

let searchTimeout = null;


animeSearch.addEventListener(
    "input",
    () => {

        const recherche =
            animeSearch.value.trim();


        clearTimeout(
            searchTimeout
        );


        if (recherche.length < 3) {

            searchResults.innerHTML = "";

            return;
        }


        searchTimeout =
            setTimeout(
                () => {

                    searchAniList(
                        recherche
                    );

                },
                300
            );

    }
);


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
                            anime.title.romaji;

                        const titreSecondaire =
                            anime.title.romaji;


                        return `
                            <article
                                class="search-result"
                            >

                                <img
                                class="search-result-image"
                                src="${anime.image}"
                                alt="${titrePrincipal}"
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

async function handleAddAnime(event) {

    const button =
        event.currentTarget;


    const anilistId =
        Number(
            button.dataset.anilistId
        );

    currentAnimeToAdd = anilistId;


    seasonCountInput.value = 1;


    addModal.style.display = "flex";


    return;

    try {

        const response =
            await fetch(
                "/add-anime/"
                + anilistId,
                {
                    method: "POST",

                    headers: {
                        "Content-Type": "application/json"
                    },

                    body: JSON.stringify({
                        nombre_saisons: nombreSaisons
                    })
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

cancelAddButton.addEventListener(
    "click",
    () => {

        addModal.style.display = "none";

        currentAnimeToAdd = null;

    }
);


confirmAddButton.addEventListener(
    "click",
    async () => {


        const nombreSaisons =
            Number(
                seasonCountInput.value
            );


        if (
            !nombreSaisons ||
            nombreSaisons < 1
        ) {

            alert(
                "Nombre de saisons invalide."
            );

            return;

        }


        try {

            const response =
                await fetch(
                    "/add-anime/"
                    + currentAnimeToAdd,
                    {
                        method: "POST",

                        headers: {
                            "Content-Type": "application/json"
                        },

                        body: JSON.stringify({
                            nombre_saisons:
                                nombreSaisons
                        })
                    }
                );


            const resultat =
                await response.json();


            if (!resultat.success) {

                throw new Error();

            }


            addModal.style.display = "none";


            loadAnimes();


        } catch(error) {

            console.error(error);

            alert(
                "Erreur pendant l'ajout."
            );

        }

    }
);

document.addEventListener(
    "click",
    (event) => {

        const clicDansRecherche =
            animeSearch.contains(event.target);


        const clicDansResultats =
            searchResults.contains(event.target);


        // Si le clic n'est pas dans la recherche
        // ni dans les résultats
        if (
            !clicDansRecherche &&
            !clicDansResultats
        ) {

            animeSearch.value = "";

            searchResults.innerHTML = "";

        }

    }
);

const librarySearch =
    document.getElementById("search");


document.addEventListener(
"click",
(event) => {

    const clicDansRecherche =
        librarySearch.contains(event.target);

    if (!clicDansRecherche) {

        librarySearch.value = "";

        displayAnimes("");

    }
}
);

loadAnimes();
