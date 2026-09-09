
let animes = [];
const animeList = document.getElementById("anime-list");
const librarySearch = document.getElementById("search");
const animeSearch = document.getElementById("anime-search");
const searchResults = document.getElementById("search-results");
const animeSearchDelay = 300;
const unknownOriginalTitle = "Titre original inconnu";

loadMedia("/anime/api", (medias) => {
    animes = medias;
}, animeList, "anime", "animes", unknownOriginalTitle);


function displayAnimes(search = "") {
    displayMedia(animes, search, animeList, "anime", unknownOriginalTitle);
}

function handleLibrarySearch() {
    const recherche = librarySearch.value.trim();
    const rechercheTropCourte = recherche.length < minimumSearchLength;
    if (rechercheTropCourte) {
        displayAnimes("");
        return;
    }
    displayAnimes(recherche);
}

librarySearch.addEventListener("input", handleLibrarySearch);
animeSearch.addEventListener("input", () => {
    handleMediaSearch(animeSearch, searchResults, "/anime/search-anime", (resultats) => {
        displaySearchResultsMedia(resultats, searchResults, "anime", unknownOriginalTitle, (event) => {
                handleAddMedia(event, "/anime/add-anime", "/anime/api", (medias) => {
                    animes = medias;
                }, animeList, "anime", "animes", unknownOriginalTitle, animerAnimeAjoute);
        });
    }, animeSearchDelay);
});

document.addEventListener("click", (event) => {
        handleDocumentClick(event, animeSearch, searchResults, librarySearch, displayAnimes);
});

function animerAnimeAjoute(animeId) {
    const selector = `.anime-card[data-anime-id="${animeId}"]`;
    const card = document.querySelector(selector);
    if (!card) {
        return;
    }
    card.classList.add("magic-card");
}