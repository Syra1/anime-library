
let series = [];
const serieList = document.getElementById("serie-list");
const librarySearch = document.getElementById("search");
const serieSearch = document.getElementById("serie-search");
const searchResults = document.getElementById("search-results");
const serieSearchDelay = 300;
const unknownOriginalTitle = "Titre original inconnu";

loadMedia("/serie/api", (medias) => {
    series = medias;
}, serieList, "serie", "series", unknownOriginalTitle);


function displaySeries(search = "") {
    displayMedia(series, search, serieList, "serie", unknownOriginalTitle);
}

function handleLibrarySearch() {
    const recherche = librarySearch.value.trim();
    const rechercheTropCourte = recherche.length < minimumSearchLength;
    if (rechercheTropCourte) {
        displaySeries("");
        return;
    }
    displaySeries(recherche);
}

librarySearch.addEventListener("input", handleLibrarySearch);
serieSearch.addEventListener("input", () => {
    handleMediaSearch(serieSearch, searchResults, "/serie/search-serie", (resultats) => {
        displaySearchResultsMedia(resultats, searchResults, "serie", unknownOriginalTitle, (event) => {
                handleAddMedia(event, "/serie/add-serie", "/serie/api", (medias) => {
                    series = medias;
                }, serieList, "serie", "series", unknownOriginalTitle, animerSerieAjoute);
        });
    }, serieSearchDelay);
});

document.addEventListener("click", (event) => {
        handleDocumentClick(event, serieSearch, searchResults, librarySearch, displaySeries);
});

function animerSerieAjoute(serieId) {
    const selector = `.serie-card[data-serie-id="${serieId}"]`;
    const card = document.querySelector(selector);
    if (!card) {
        return;
    }
    card.classList.add("magic-card");
}