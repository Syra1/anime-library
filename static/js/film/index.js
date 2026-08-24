// Déclaration des variables

let films = [];

let librarySearchTimeout = null;

let searchTimeout = null;

const filmList = document.getElementById("film-list");

const librarySearch = document.getElementById("search");

const filmSearch = document.getElementById("film-search");

const searchResults = document.getElementById("search-results");

const minimumSearchLength = 3;

const filmSearchDelay = 300;

const filmAnimationDelay = 100;

const unknownOriginalTitle = "Titre original inconnu";


// Charge les films depuis la base de données.

async function loadFilms() {

    try {

        const response = await fetch("/film/api");

        if (!response.ok) {

            throw new Error(
                "Erreur lors du chargement des films"
            );

        }

        const resultats = await response.json();

        films = resultats;

        displayFilms();

    } catch (error) {

        console.error(error);

        const message = `
            <p>Impossible de charger les films.</p>
        `;

        filmList.innerHTML = message;
    }
}


// Normalise les noms pour la recherche,
// sans accents ni majuscules.

function normalizeText(text) {

    return (text || "")
        .normalize("NFD")
        .replace(/[\u0300-\u036f]/g, "")
        .toLowerCase();
}


// Filtre les films, génère leurs cartes
// et les affiche dans la bibliothèque.

function displayFilms(search = "") {

    const recherche = normalizeText(search);

    const filteredFilms = films.filter(film => {

        const titre = normalizeText(
            film.titre
        );

        const titreOriginal = normalizeText(
            film.titre_original
        );

        return (
            titre.includes(recherche) ||
            titreOriginal.includes(recherche)
        );
    });


    const aucunResultat =
        filteredFilms.length === 0;


    if (aucunResultat) {

        const message = `
            <p>Aucun film trouvé.</p>
        `;

        filmList.innerHTML = message;

        return;
    }


    const filmCards = filteredFilms

        .map(film => {

            const titre = film.titre;

            const titreOriginal =
                film.titre_original ||
                unknownOriginalTitle;

            const image = film.image;

            const filmId = film.id;



            return `

                <a
                    href="/film/${filmId}"
                    class="film-card"
                    data-film-id="${filmId}"
                >

                    <div class="film-image">

                        <img
                            src="${image}"
                            alt="${titre}"
                        >

                    </div>


                    <div class="film-info">

                        <h2>
                            ${titre}
                        </h2>

                        <p class="original-title">
                            ${titreOriginal}
                        </p>

                    </div>

                </a>

            `;

        })

        .join("");


    filmList.innerHTML = filmCards;
}


// Gère la saisie dans le champ de recherche
// de la bibliothèque.

function handleLibrarySearch() {

    clearTimeout(librarySearchTimeout);

    const recherche =
        librarySearch.value.trim();


    const rechercheTropCourte =
        recherche.length < minimumSearchLength;


    if (rechercheTropCourte) {

        displayFilms("");

        return;
    }


    displayFilms(recherche);
}


librarySearch.addEventListener(
    "input",
    handleLibrarySearch
);


// Gère la saisie dans le champ
// de recherche TMDB.

function handleFilmSearch() {

    const recherche =
        filmSearch.value.trim();


    clearTimeout(searchTimeout);


    const rechercheTropCourte =
        recherche.length < minimumSearchLength;


    if (rechercheTropCourte) {

        searchResults.innerHTML = "";

        return;
    }


    searchTimeout = setTimeout(() => {

        searchTMDB(recherche);

    }, filmSearchDelay);
}


filmSearch.addEventListener(
    "input",
    handleFilmSearch
);


// Recherche un film via l'API TMDB.

async function searchTMDB(recherche) {

    const loadingMessage = `
        <p>Recherche en cours...</p>
    `;

    searchResults.innerHTML =
        loadingMessage;


    try {

        const encodedRecherche =
            encodeURIComponent(recherche);


        const url =
            "/film/search-film?q=" +
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


        displaySearchResults(resultats);


    } catch (error) {

        console.error(error);


        const errorMessage = `
            <p>
                Impossible de rechercher ce film.
            </p>
        `;

        searchResults.innerHTML =
            errorMessage;
    }
}


// Affiche les résultats de la recherche TMDB.

function displaySearchResults(resultats) {

    const aucunResultat =
        !resultats ||
        resultats.length === 0;


    if (aucunResultat) {

        const message = `
            <p>Aucun film trouvé.</p>
        `;

        searchResults.innerHTML =
            message;

        return;
    }


    const searchResultsList = resultats

        .map(film => {

            const titre =
                film.title;

            const titreOriginal =
                film.original_title ||
                unknownOriginalTitle;

            const image =
                film.image;

            const annee =
                film.annee;

            const tmdbId =
                film.id;


            return `

                <article class="search-result">

                    <img
                        class="search-result-image"
                        src="${image}"
                        alt="${titre}"
                    >


                    <div class="search-result-info">

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
                        class="add-film-button"
                        data-tmdb-id="${tmdbId}"
                    >
                        Ajouter
                    </button>

                </article>

            `;

        })

        .join("");


    const searchResultsHTML = `

        <div class="search-results-list">

            ${searchResultsList}

        </div>

    `;


    searchResults.innerHTML =
        searchResultsHTML;


    const addFilmButtons =
        document.querySelectorAll(
            ".add-film-button"
        );


    addFilmButtons.forEach(button => {

        button.addEventListener(
            "click",
            handleAddFilm
        );

    });
}


// Ajoute directement le film
// dans la base de données.

async function handleAddFilm(event) {

    const button = event.currentTarget;

    const tmdbId = Number(
        button.dataset.tmdbId
    );

    if (!tmdbId) {
        return;
    }


    // Évite plusieurs clics pendant l'ajout.

    button.disabled = true;

    button.textContent = "Ajout...";


    try {

        const url =
            "/film/add-film/" +
            tmdbId;


        const response = await fetch(
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
                "L'ajout du film a échoué"
            );

        }


        // Recharge la bibliothèque.

        await loadFilms();


        const filmId =
            resultat.film_id;


        setTimeout(() => {

            animerFilmAjoute(
                filmId
            );

        }, filmAnimationDelay);


        // Le résultat de recherche reste affiché.

        button.textContent = "Ajouté";


    } catch (error) {

        console.error(error);

        alert(
            "Erreur pendant l'ajout du film."
        );


        button.disabled = false;

        button.textContent = "Ajouter";
    }
}


// Ferme les recherches lorsqu'un clic
// est effectué en dehors des barres.

function handleDocumentClick(event) {

    const clicDansRecherche =
        filmSearch.contains(
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


    const clicEnDehorsRechercheFilm =
        !clicDansRecherche &&
        !clicDansResultats;


    const clicEnDehorsRechercheBibliotheque =
        !clicDansLibrarySearch;


    if (clicEnDehorsRechercheFilm) {

        filmSearch.value = "";

        searchResults.innerHTML = "";
    }


    if (
        clicEnDehorsRechercheBibliotheque
    ) {

        librarySearch.value = "";

        displayFilms("");
    }
}


document.addEventListener(
    "click",
    handleDocumentClick
);


// Prépare la nouvelle card
// pour l'animation CSS.

function animerFilmAjoute(filmId) {

    const selector =
        `.film-card[data-film-id="${filmId}"]`;


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


// Recharge la liste des films
// depuis la base de données.

loadFilms();