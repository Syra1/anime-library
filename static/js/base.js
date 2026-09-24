
const searchButton = document.querySelector("#search-button");
const closeButton = document.querySelector("#close-button");
const addButton = document.querySelector("#add-button");
const sideMenu = document.querySelector("#side-menu");
const sideMenuOverlay = document.querySelector("#side-menu-overlay");

const searchContent = document.querySelector(".search-content");
const addContent = document.querySelector(".add-content");

function normalizeText(text) {
    return (text || "")
        .normalize("NFD")
        .replace(/[\u0300-\u036f]/g, "")
        .toLowerCase()
        .trim();
}

searchButton.addEventListener("click", () => {
    sideMenu.classList.add("visible");
    sideMenuOverlay.classList.add("visible");

    searchContent.style.display = "block";
    addContent.style.display = "none";

    addButton.style.visibility = "hidden";
    searchButton.style.visibility = "hidden";
});

addButton.addEventListener("click", () => {
    sideMenu.classList.add("visible");
    sideMenuOverlay.classList.add("visible");

    searchContent.style.display = "none";
    addContent.style.display = "block";

    addButton.style.visibility = "hidden";
    searchButton.style.visibility = "hidden";
});

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
        `#${mediaType.toLowerCase()}-side-search`
    );

    const searchResults = document.querySelector(
        `#${mediaType}-search-results`
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