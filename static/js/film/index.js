
let films = [];
const filmList = document.getElementById("film-list");
const librarySearch = document.getElementById("search");
const filmSearch = document.getElementById("film-search");
const searchResults = document.getElementById("search-results");
const filmSearchDelay = 300;
const unknownOriginalTitle = "Titre original inconnu";

loadMedia("/film/api", (medias) => {
    films = medias;
}, filmList, "film", "films", unknownOriginalTitle);


function displayFilms(search = "") {
    displayMedia(films, search, filmList, "film", unknownOriginalTitle);
}

function handleLibrarySearch() {
    const recherche = librarySearch.value.trim();
    const rechercheTropCourte = recherche.length < minimumSearchLength;
    if (rechercheTropCourte) {
        displayFilms("");
        return;
    }
    displayFilms(recherche);
}

librarySearch.addEventListener("input", handleLibrarySearch);
filmSearch.addEventListener("input", () => {
    handleMediaSearch(filmSearch, searchResults, "/film/search-film", (resultats) => {
        displaySearchResultsMedia(resultats, searchResults, "film", unknownOriginalTitle, (event) => {
                handleAddMedia(event, "/film/add-film", "/film/api", (medias) => {
                    films = medias;
                }, filmList, "film", "films", unknownOriginalTitle, animerFilmAjoute);
        });
    }, filmSearchDelay);
});

document.addEventListener("click", (event) => {
        handleDocumentClick(event, filmSearch, searchResults, librarySearch, displayFilms);
});

function animerFilmAjoute(filmId) {
    const selector = `.film-card[data-film-id="${filmId}"]`;
    const card = document.querySelector(selector);
    if (!card) {
        return;
    }
    card.classList.add("magic-card");
}