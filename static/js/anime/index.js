// Déclaration des variables

let animes = [];


let searchTimeout = null;

const animeList =
    document.getElementById("anime-list");

const librarySearch =
    document.getElementById("search");

const animeSearch =
    document.getElementById("anime-search");

const searchResults =
    document.getElementById("search-results");

const minimumSearchLength = 3;

const animeSearchDelay = 300;

const animeAnimationDelay = 100;

const unknownOriginalTitle =
    "Titre original inconnu";


// Charge les animes depuis la base de données.

async function loadSéries() {

    try {

        const response =
            await fetch("/anime/api");

        if (!response.ok) {

            throw new Error(
                "Erreur lors du chargement des animes"
            );

        }

        const resultats =
            await response.json();

        animes = Array.isArray(resultats)
            ? resultats
            : [];

        displaySéries();

    } catch (error) {

        console.error(
            "Erreur chargement animes :",
            error
        );

        const message = `
            <p>Impossible de charger les animes.</p>
        `;

        animeList.innerHTML = message;
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

// Génère une carte de anime.

function createSérieCard(anime) {

    const titre =
        anime.titre || "Titre inconnu";


    const titreOriginal =
        anime.titre_original ||
        unknownOriginalTitle;

    const realisateur =
        anime.realisateur;


    const image =
        anime.image;


    const animeId =
        anime.id;


    return `
        <div class="anime-card-background">
            <a
                href="/anime/${animeId}"
                class="anime-card"
                data-anime-id="${animeId}"
            >

                <div class="anime-image">

                    <img
                        src="${image || ""}"
                        alt="${titre}"
                    >

                </div>


                <div class="anime-info">

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


// Filtre les animes, les trie par nom,
// génère leurs cartes et les affiche
// dans la bibliothèque.

// Filtre les animes,
// génère leurs cartes et les affiche
// dans la bibliothèque.

function displaySéries(search = "") {

    const recherche =
        normalizeText(search);


    const filteredSéries =
        animes.filter(
            anime => {

                const titre =
                    normalizeText(
                        anime.titre
                    );


                const titreOriginal =
                    normalizeText(
                        anime.titre_original
                    );


                return (
                    titre.includes(recherche) ||
                    titreOriginal.includes(recherche)
                );

            }
        );


    if (filteredSéries.length === 0) {

        animeList.innerHTML = `
            <p>Aucun anime trouvé.</p>
        `;

        return;
    }


    const animeCards =
        filteredSéries
            .map(createSérieCard)
            .join("");


    animeList.innerHTML =
        animeCards;
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
        animeSearch.value.trim();


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
            animeSearchDelay
        );
}


animeSearch.addEventListener(
    "input",
    handleSérieSearch
);


// Recherche un anime via l'API TMDB.

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
            "/anime/search-anime?q=" +
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
                Impossible de rechercher ce anime.
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
                                class="add-anime-button"
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

        await loadSéries();


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


// Recharge la liste des animes
// depuis la base de données.

loadSéries();