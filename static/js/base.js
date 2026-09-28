const mediaAnimationDelay = 100;

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

// Ferme le side-menu si il y a un clique en dehors du side-menu
document.addEventListener("click", (event) => {
    const clicDansMenu = sideMenu.contains(event.target);
    const clicSurBoutonOuverture = searchButton.contains(event.target) || addButton.contains(event.target);

    if (!clicDansMenu && !clicSurBoutonOuverture) {
        sideMenu.classList.remove("visible");
        sideMenuOverlay.classList.remove("visible");

        addButton.style.visibility = "visible";
        searchButton.style.visibility = "visible";
        closeButton.style.visibility = "hidden"
    }
});

// Seelctionne le contenu d'une barre de recherche si il y a deja du contenu
const mediaSearchInputs = document.querySelectorAll(".media-search");

mediaSearchInputs.forEach((input) => {
    input.addEventListener("focus", () => {
        input.select();
    });
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

        if (recherche.length < minimumSearchLength) {
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

function displaySearchResultsMedia(
    resultats,
    searchResults,
    typeMedia,
    unknownOriginalTitle,
    addMedia
) {
    const aucunResultat =
        !Array.isArray(resultats) || resultats.length === 0;

    if (aucunResultat) {
        searchResults.innerHTML = `<p>Aucun ${typeMedia} trouvé.</p>`;
        return;
    }

    const searchResultsList = resultats.map(media => {
        const titre = media.title || "Titre inconnu";
        const titreOriginal =
            media.original_title || unknownOriginalTitle;
        const image = media.image;
        const annee = media.annee;
        const tmdbId = media.id;

        return `
            <article class="search-result">

                <img
                    class="search-result-image"
                    src="${image || ""}"
                    alt="${titre}"
                >

                <div class="search-result-info">
                    <h3>${titre}</h3>
                    <p>${titreOriginal}</p>
                    ${annee ? `<p>${annee}</p>` : ""}
                </div>

                <button
                    type="button"
                    class="add-${typeMedia}-button add-media-button"
                    data-tmdb-id="${tmdbId}"
                >
                    Ajouter
                </button>

            </article>
        `;
    }).join("");

    searchResults.innerHTML = searchResultsList;

    const addMediaButtons = searchResults.querySelectorAll(
        `.add-${typeMedia}-button`
    );

    addMediaButtons.forEach(button => {
        button.addEventListener("click", addMedia);
    });
}

// Ajouter un media
async function handleAddMedia(event, addUrl, loadUrl, setMedia, mediaList, typeMedia, mediaName, unknownOriginalTitle, animateMedia) {
    const button = event.currentTarget;
    const tmdbId = Number(button.dataset.tmdbId);
    if (!tmdbId) {
        return;
    }
    button.disabled = true;
    button.textContent = "Ajout...";
    try {
        const response = await fetch(`${addUrl}/${tmdbId}`, {
            method: "POST"
        });
        if (!response.ok) {
            throw new Error("Erreur HTTP lors de l'ajout");
        }
        const resultat = await response.json();
        if (!resultat.success) {
            throw new Error(`L'ajout du ${mediaName} a échoué`);
        }
        if (mediaList) {
            await loadMedia(loadUrl, setMedia, mediaList, typeMedia, mediaName, unknownOriginalTitle);
        }
        const mediaId = resultat[`${typeMedia}_id`];
        setTimeout(() => {
            animateMedia(mediaId);
        }, mediaAnimationDelay);
        button.textContent = "Ajouté";
        button.disabled = true;
    } catch (error) {
        console.error(`Erreur ajout ${mediaName} :`, error);
        alert(`Erreur pendant l'ajout du ${mediaName}.`);
        button.disabled = false;
        button.textContent = "Ajouter";
    }
}




const addMediaTypes = [
    {
        type: "anime",
        name: "animes",
        searchUrl: "/anime/search-anime",
        addUrl: "/anime/add-anime"
    },
    {
        type: "film",
        name: "films",
        searchUrl: "/film/search-film",
        addUrl: "/film/add-film"
    },
    {
        type: "serie",
        name: "series",
        searchUrl: "/serie/search-serie",
        addUrl: "/serie/add-serie"
    }
];

addMediaTypes.forEach((media) => {

    const searchInput = document.querySelector(
        `#add-${media.type}-side-search`
    );

    const searchResults = document.querySelector(
        `#add-${media.type.charAt(0).toUpperCase() + media.type.slice(1)}-search-results`
    );

    searchInput.addEventListener("input", () => {

        handleMediaSearch(
            searchInput,
            searchResults,
            media.searchUrl,
            (resultats) => {

                displaySearchResultsMedia(
                    resultats,
                    searchResults,
                    media.type,
                    "Titre original inconnu",
                    (event) => {

                        handleAddMedia(
                            event,
                            media.addUrl,
                            `/${media.type}/api`,
                            () => {},
                            null,
                            media.type,
                            media.name,
                            "Titre original inconnu",
                            () => {}
                        );

                    }
                );

            },
            300
        );

    });

});