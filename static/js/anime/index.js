// Déclaration des variables

let animes = [];


const animeList =
    document.getElementById("anime-list");

const librarySearch =
    document.getElementById("search");

const animeSearch =
    document.getElementById("anime-search");

const searchResults =
    document.getElementById("search-results");


const animeSearchDelay = 300;

const animeAnimationDelay = 100;

const unknownOriginalTitle =
    "Titre original inconnu";


// Charge les animes depuis la base de données.

loadMedia(
    "/anime/api",
    (medias) => {
        animes = medias;
    },
    animeList,
    "anime",
    "animes",
    unknownOriginalTitle
);


function displayAnimes(search = "") {

    displayMedia(
        animes,
        search,
        animeList,
        "anime",
        unknownOriginalTitle
    );

}


// Gère la saisie dans le champ de recherche
// de la bibliothèque.

function handleLibrarySearch() {

    const recherche =
        librarySearch.value.trim();

    const rechercheTropCourte =
        recherche.length <
        minimumSearchLength;

    if (rechercheTropCourte) {

        displayAnimes("");

        return;
    }

    displayAnimes(
        recherche
    );

}


librarySearch.addEventListener(
    "input",
    handleLibrarySearch
);


// Gère la saisie dans le champ
// de recherche TMDB.

animeSearch.addEventListener(
    "input",
    () => {
        handleMediaSearch(
            animeSearch,
            searchResults,
            "/anime/search-anime",
            displaySearchResults,
            animeSearchDelay
        );
    }
);


// Affiche les résultats de la recherche TMDB.

function displaySearchResults(
    resultats
) {

    const aucunResultat =
        !Array.isArray(resultats) ||
        resultats.length === 0;


    if (aucunResultat) {

        const message = `
            <p>Aucun anime trouvé.</p>
        `;


        searchResults.innerHTML =
            message;


        return;
    }


    const searchResultsList =
        resultats
            .map(
                anime => {

                    const titre =
                        anime.title ||
                        "Titre inconnu";


                    const titreOriginal =
                        anime.original_title ||
                        unknownOriginalTitle;


                    const image =
                        anime.image;


                    const annee =
                        anime.annee;


                    const tmdbId =
                        anime.id;


                    return `

                        <article
                            class="search-result"
                        >

                            <img
                                class="search-result-image"
                                src="${image || ""}"
                                alt="${titre}"
                            >


                            <div
                                class="search-result-info"
                            >

                                <h3>
                                    ${titre}
                                </h3>


                                <p>
                                    ${titreOriginal}
                                </p>


                                ${
                                    annee
                                        ? `
                                            <p>
                                                ${annee}
                                            </p>
                                        `
                                        : ""
                                }

                            </div>


                            <button
                                class="add-anime-button add-media-button"
                                data-tmdb-id="${tmdbId}"
                            >
                                Ajouter
                            </button>

                        </article>

                    `;

                }
            )
            .join("");


    const searchResultsHTML = `

        <div
            class="search-results-list"
        >

            ${searchResultsList}

        </div>

    `;


    searchResults.innerHTML =
        searchResultsHTML;


    const addSérieButtons =
        document.querySelectorAll(
            ".add-anime-button"
        );


    addSérieButtons.forEach(
        button => {

            button.addEventListener(
                "click",
                handleAddSérie
            );

        }
    );
}


// Ajoute directement le anime
// dans la base de données.

async function handleAddSérie(event) {

    const button =
        event.currentTarget;


    const tmdbId =
        Number(
            button.dataset.tmdbId
        );


    if (!tmdbId) {

        return;
    }


    // Évite plusieurs clics
    // pendant l'ajout.

    button.disabled =
        true;


    button.textContent =
        "Ajout...";


    try {

        const url =
            "/anime/add-anime/" +
            tmdbId;


        const response =
            await fetch(
                url,
                {
                    method: "POST"
                }
            );


        if (!response.ok) {

            throw new Error(
                "Erreur HTTP lors de l'ajout"
            );

        }


        const resultat =
            await response.json();


        if (!resultat.success) {

            throw new Error(
                "L'ajout du anime a échoué"
            );

        }


        // Recharge la bibliothèque.

        await loadMedia(
            "/anime/api",
            (medias) => {
                animes = medias;
            },
            animeList,
            "anime",
            "animes",
            unknownOriginalTitle
        );


        const animeId =
            resultat.anime_id;


        setTimeout(
            () => {

                animerSérieAjoute(
                    animeId
                );

            },
            animeAnimationDelay
        );


        button.textContent =
            "Ajouté";


    } catch (error) {

        console.error(
            "Erreur ajout anime :",
            error
        );


        alert(
            "Erreur pendant l'ajout du anime."
        );


        button.disabled =
            false;


        button.textContent =
            "Ajouter";
    }
}


// Ferme les recherches lorsqu'un clic
// est effectué en dehors des barres.

function handleDocumentClick(event) {

    const clicDansRecherche =
        animeSearch.contains(
            event.target
        );


    const clicDansResultats =
        searchResults.contains(
            event.target
        );


    const clicDansLibrarySearch =
        librarySearch.contains(
            event.target
        );


    const clicEnDehorsRechercheSérie =
        !clicDansRecherche &&
        !clicDansResultats;


    const clicEnDehorsRechercheBibliotheque =
        !clicDansLibrarySearch;


    if (clicEnDehorsRechercheSérie) {

        animeSearch.value =
            "";

        searchResults.innerHTML =
            "";
    }


    if (clicEnDehorsRechercheBibliotheque) {

        if (librarySearch.value !== "") {

            librarySearch.value = "";

            displayAnimes("");

    }
}
}


document.addEventListener(
    "click",
    handleDocumentClick
);


// Prépare la nouvelle card
// pour l'animation CSS.

function animerSérieAjoute(
    animeId
) {

    const selector =
        `.anime-card[data-anime-id="${animeId}"]`;


    const card =
        document.querySelector(
            selector
        );


    if (!card) {

        return;
    }


    card.classList.add(
        "magic-card"
    );
}