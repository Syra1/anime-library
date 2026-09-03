// Déclaration des variables

let series = [];


let searchTimeout = null;

const serieList =
    document.getElementById("serie-list");

const librarySearch =
    document.getElementById("search");

const serieSearch =
    document.getElementById("serie-search");

const searchResults = document.getElementById("search-results");

const minimumSearchLength = 3;

const serieSearchDelay = 300;

const serieAnimationDelay = 100;

const unknownOriginalTitle =
    "Titre original inconnu";


// Charge les series depuis la base de données.

async function loadSéries() {

    try {

        const response =
            await fetch("/serie/api");

        if (!response.ok) {

            throw new Error(
                "Erreur lors du chargement des series"
            );

        }

        const resultats =
            await response.json();

        series = Array.isArray(resultats)
            ? resultats
            : [];

        displaySéries();

    } catch (error) {

        console.error(
            "Erreur chargement series :",
            error
        );

        const message = `
            <p>Impossible de charger les series.</p>
        `;

        serieList.innerHTML = message;
    }
}


// Normalise les noms pour la recherche
// et le tri, sans accents ni majuscules.

function normalizeText(text) {

    return (text || "")
        .normalize("NFD")
        .replace(/[\u0300-\u036f]/g, "")
        .toLowerCase()
        .trim();
}

// Génère une carte de serie.

function createSérieCard(serie) {

    const titre =
        serie.titre || "Titre inconnu";


    const titreOriginal =
        serie.titre_original ||
        unknownOriginalTitle;

    const realisateur =
        serie.realisateur;


    const image =
        serie.image;


    const serieId =
        serie.id;


    return `
        <div class="media-card-background">
            <a
                href="/serie/${serieId}"
                class="serie-card media-card"
                data-serie-id="${serieId}"
            >

                <div class="media-image">

                    <img
                        src="${image || ""}"
                        alt="${titre}"
                    >

                </div>


                <div class="media-info">

                    <h2>
                        ${titre}
                    </h2>

                    <p class="original-title">
                        ${titreOriginal}
                    </p>

                </div>

            </a>
        </div>

    `;
}


// Filtre les series, les trie par nom,
// génère leurs cartes et les affiche
// dans la bibliothèque.

// Filtre les series,
// génère leurs cartes et les affiche
// dans la bibliothèque.

function displaySéries(search = "") {

    const recherche =
        normalizeText(search);


    const filteredSéries =
        series.filter(
            serie => {

                const titre =
                    normalizeText(
                        serie.titre
                    );


                const titreOriginal =
                    normalizeText(
                        serie.titre_original
                    );


                return (
                    titre.includes(recherche) ||
                    titreOriginal.includes(recherche)
                );

            }
        );


    if (filteredSéries.length === 0) {

        serieList.innerHTML = `
            <p>Aucun serie trouvé.</p>
        `;

        return;
    }


    const serieCards =
        filteredSéries
            .map(createSérieCard)
            .join("");


    serieList.innerHTML =
        serieCards;
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

        displaySéries("");

        return;
    }


    displaySéries(
        recherche
    );
}


librarySearch.addEventListener(
    "input",
    handleLibrarySearch
);


// Gère la saisie dans le champ
// de recherche TMDB.

function handleSérieSearch() {

    const recherche =
        serieSearch.value.trim();


    clearTimeout(
        searchTimeout
    );


    const rechercheTropCourte =
        recherche.length <
        minimumSearchLength;


    if (rechercheTropCourte) {

        searchResults.innerHTML =
            "";

        return;
    }


    searchTimeout =
        setTimeout(
            () => {

                searchTMDB(
                    recherche
                );

            },
            serieSearchDelay
        );
}


serieSearch.addEventListener(
    "input",
    handleSérieSearch
);


// Recherche un serie via l'API TMDB.

async function searchTMDB(
    recherche
) {

    const loadingMessage = `
        <p>Recherche en cours...</p>
    `;


    searchResults.innerHTML =
        loadingMessage;


    try {

        const encodedRecherche =
            encodeURIComponent(
                recherche
            );


        const url =
            "/serie/search-serie?q=" +
            encodedRecherche;


        const response =
            await fetch(url);


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

        console.error(
            "Erreur recherche TMDB :",
            error
        );


        const errorMessage = `
            <p>
                Impossible de rechercher ce serie.
            </p>
        `;


        searchResults.innerHTML =
            errorMessage;
    }
}


// Affiche les résultats de la recherche TMDB.

function displaySearchResults(
    resultats
) {

    const aucunResultat =
        !Array.isArray(resultats) ||
        resultats.length === 0;


    if (aucunResultat) {

        const message = `
            <p>Aucun serie trouvé.</p>
        `;


        searchResults.innerHTML =
            message;


        return;
    }


    const searchResultsList =
        resultats
            .map(
                serie => {

                    const titre =
                        serie.title ||
                        "Titre inconnu";


                    const titreOriginal =
                        serie.original_title ||
                        unknownOriginalTitle;


                    const image =
                        serie.image;


                    const annee =
                        serie.annee;


                    const tmdbId =
                        serie.id;


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
                                class="add-serie-button add-media-button"
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
            ".add-serie-button"
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


// Ajoute directement le serie
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
            "/serie/add-serie/" +
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
                "L'ajout du serie a échoué"
            );

        }


        // Recharge la bibliothèque.

        await loadSéries();


        const serieId =
            resultat.serie_id;


        setTimeout(
            () => {

                animerSérieAjoute(
                    serieId
                );

            },
            serieAnimationDelay
        );


        button.textContent =
            "Ajouté";


    } catch (error) {

        console.error(
            "Erreur ajout serie :",
            error
        );


        alert(
            "Erreur pendant l'ajout du serie."
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
        serieSearch.contains(
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

        serieSearch.value =
            "";

        searchResults.innerHTML =
            "";
    }


    if (clicEnDehorsRechercheBibliotheque) {

        if (librarySearch.value !== "") {

            librarySearch.value = "";

            displaySéries("");

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
    serieId
) {

    const selector =
        `.serie-card[data-serie-id="${serieId}"]`;


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


// Recharge la liste des series
// depuis la base de données.

loadSéries();