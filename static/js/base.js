
const searchButton = document.querySelector("#search-button");
const closeButton = document.querySelector("#close-button");
const addButton = document.querySelector("#add-button");
const sideMenu = document.querySelector("#side-menu");
const sideMenuOverlay = document.querySelector("#side-menu-overlay");

const searchContent = document.querySelector(".search-content");
const addContent = document.querySelector(".add-content");

let searchTimeout = null;
const minimumSearchLength = 3;

function normalizeText(text) {
    return (text || "")
        .normalize("NFD")
        .replace(/[\u0300-\u036f]/g, "")
        .toLowerCase()
        .trim();
}

// Bouton Ajouter side-menu de header-bar
addButton.addEventListener("click", () => {
    sideMenu.classList.add("visible");
    sideMenuOverlay.classList.add("visible");

    searchContent.style.display = "none";
    addContent.style.display = "block";

    addButton.style.visibility = "hidden";
    searchButton.style.visibility = "visible";
    closeButton.style.visibility = "visible"
});

// Bouton Rechercher side-menu de header-bar
searchButton.addEventListener("click", () => {
    sideMenu.classList.add("visible");
    sideMenuOverlay.classList.add("visible");

    searchContent.style.display = "block";
    addContent.style.display = "none";

    addButton.style.visibility = "visible";
    searchButton.style.visibility = "hidden";
    closeButton.style.visibility = "visible"
});

// Bouton Fermer side-menu de header-bar
closeButton.addEventListener("click", () => {
    sideMenu.classList.add("visible");
    sideMenuOverlay.classList.add("visible");

    searchContent.style.display = "none";
    addContent.style.display = "block";

    addButton.style.visibility = "visible";
    searchButton.style.visibility = "visible";
    closeButton.style.visibility = "hidden"
});

// Seelctionne le contenu d'une barre de recherch si il y a deja du contenu
const mediaSearchInputs = document.querySelectorAll(".media-search");

mediaSearchInputs.forEach((input) => {
    input.addEventListener("focus", () => {
        input.select();
    });
});

// Ferme le side-menu si il y a un clique en dehors du side-menu
document.addEventListener("click", (event) => {
    const clicDansMenu = sideMenu.contains(event.target);
    const clicSurBoutonOuverture = searchButton.contains(event.target) || addButton.contains(event.target);

    if (!clicDansMenu && !clicSurBoutonOuverture) {
        sideMenu.classList.remove("visible");
        sideMenuOverlay.classList.remove("visible");

        addButton.style.visibility = "visible";
        searchButton.style.visibility = "visible";
    }
});


// Ouvre le sous-menu de side-menu qui correspond a la page actuel
const searchCategoryButtons = searchContent.querySelectorAll(".category-side-menu button");
const searchMenuPages = searchContent.querySelectorAll(".page-menu");

const addCategoryButtons = addContent.querySelectorAll(".category-side-menu button");
const addMenuPages = addContent.querySelectorAll(".page-menu");

const chemin = window.location.pathname;

let pageActive = 0;

if (chemin.startsWith("/film")) {
    pageActive = 1;
} else if (chemin.startsWith("/serie")) {
    pageActive = 2;
} else if (chemin.startsWith("/anime")) {
    pageActive = 0;
}

// Bouton Search
searchMenuPages.forEach((page, index) => {
    page.style.display = index === pageActive ? "flex" : "none";
});

searchCategoryButtons[pageActive].classList.add("active");

searchCategoryButtons.forEach((button, index) => {
    button.addEventListener("click", () => {
        searchMenuPages.forEach(page => {
            page.style.display = "none";
        });

        searchCategoryButtons.forEach(button => {
            button.classList.remove("active");
        });

        searchMenuPages[index].querySelector(".media-search").value = "";
        searchMenuPages[index].style.display = "flex";
        button.classList.add("active");
    });
});

// Bouton Add
addMenuPages.forEach((page, index) => {
    page.style.display = index === pageActive ? "flex" : "none";
});

addCategoryButtons[pageActive].classList.add("active");

addCategoryButtons.forEach((button, index) => {
    button.addEventListener("click", () => {
        addMenuPages.forEach(page => {
            page.style.display = "none";
        });

        addCategoryButtons.forEach(button => {
            button.classList.remove("active");
        });

        addMenuPages[index].querySelector(".media-search").value = "";
        addMenuPages[index].style.display = "flex";
        button.classList.add("active");
    });
});


// recherche Media
function rechercherMediaSideMenu(mediaType) {

    const mediaSideSearch = document.querySelector(
        `#search-${mediaType.toLowerCase()}-side-search`
    );

    const searchResults = document.querySelector(
        `#search-${mediaType}-search-results`
    );

    let medias = [];

    fetch(`/${mediaType.toLowerCase()}/api`)
        .then(response => response.json())
        .then(resultats => {
            medias = resultats;
        });

    mediaSideSearch.addEventListener("input", () => {

        const recherche = mediaSideSearch.value.trim();

        if (recherche.length < 3) {
            searchResults.innerHTML = "";
            return;
        }

        const rechercheNormalisee = normalizeText(recherche);

        const resultats = medias.filter(media => {

            const titre = normalizeText(media.titre);
            const titreOriginal = normalizeText(media.titre_original);

            return (
                titre.includes(rechercheNormalisee) ||
                titreOriginal.includes(rechercheNormalisee)
            );
        });

        searchResults.innerHTML = resultats.map(media => `

            <a href="/${mediaType.toLowerCase()}/${media.id}" class="search-result">

                <img
                    class="search-result-image"
                    src="${media.image || ""}"
                    alt="${media.titre}"
                >

                <div class="search-result-info">

                    <p>${media.titre || "Titre inconnu"}</p>

                    <p>${media.titre_original || "Titre original inconnu"}</p>

                    ${media.annee ? `<p>${media.annee}</p>` : ""}

                </div>

            </a>

        `).join("");
    });
}

rechercherMediaSideMenu("Anime");
rechercherMediaSideMenu("Film");
rechercherMediaSideMenu("Serie");

// Recherche un media sur TMDB (barre de recherche side-bar)
async function searchTMDB(recherche, url, searchResults, displaySearchResults) {
    searchResults.innerHTML = `<p>Recherche en cours...</p>`;

    try {
        const encodedRecherche = encodeURIComponent(recherche);
        const response = await fetch(`${url}?q=${encodedRecherche}`);

        if (!response.ok) {
            throw new Error("Erreur lors de la recherche");
        }

        const resultats = await response.json();

        displaySearchResults(resultats);

    } catch (error) {
        console.error("Erreur recherche TMDB :", error);
        searchResults.innerHTML = `<p>Impossible d'effectuer la recherche.</p>`;
    }
}

function handleMediaSearch(searchInput, searchResults, searchUrl, displaySearchResults, searchDelay) {
    const recherche = searchInput.value.trim();

    clearTimeout(searchTimeout);

    if (recherche.length < minimumSearchLength) {
        searchResults.innerHTML = "";
        return;
    }

    searchTimeout = setTimeout(() => {
        searchTMDB(
            recherche,
            searchUrl,
            searchResults,
            displaySearchResults
        );
    }, searchDelay);
}

function displaySearchResultsMedia(resultats, searchResults, typeMedia, unknownOriginalTitle, addMedia) {
    const aucunResultat = !Array.isArray(resultats) || resultats.length === 0;

    if (aucunResultat) {
        searchResults.innerHTML = `<p>Aucun ${typeMedia} trouvé.</p>`;
        return;
    }

    const searchResultsList = resultats.map(media => {
        const titre = media.title || "Titre inconnu";
        const titreOriginal = media.original_title || unknownOriginalTitle;
        const image = media.image;
        const annee = media.annee;
        const tmdbId = media.id;

        return `
            <article class="search-result">
                <img class="search-result-image" src="${image || ""}" alt="${titre}">
                <div class="search-result-info">
                    <h3>${titre}</h3>
                    <p>${titreOriginal}</p>
                    ${annee ? `<p>${annee}</p>` : ""}
                </div>
            </article>
        `;
    }).join("");

    searchResults.innerHTML = searchResultsList;
}

const addAnimeSearch = document.querySelector("#add-anime-side-search");
const addAnimeResults = document.querySelector("#add-Anime-search-results");

addAnimeSearch.addEventListener("input", () => {
    handleMediaSearch(
        addAnimeSearch,
        addAnimeResults,
        "/anime/search-anime",
        (resultats) => {
            displaySearchResultsMedia(
                resultats,
                addAnimeResults,
                "anime",
                "Titre original inconnu",
                () => {}
            );
        },
        300
    );
});