
const searchButton = document.querySelector("#search-button");
const closeButton = document.querySelector("#close-button");
const sideMenu = document.querySelector("#side-menu");
const sideMenuOverlay = document.querySelector("#side-menu-overlay");

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
    searchButton.style.display = "none";
    closeButton.style.display = "block";
});

closeButton.addEventListener("click", () => {
    sideMenu.classList.remove("visible");
    sideMenuOverlay.classList.remove("visible");
    closeButton.style.display = "none";
    searchButton.style.display = "block";
});

document.addEventListener("click", (event) => {
    const clicDansMenu = sideMenu.contains(event.target);
    const clicSurBoutonOuverture = searchButton.contains(event.target);

    if (!clicDansMenu && !clicSurBoutonOuverture) {
        sideMenu.classList.remove("visible");
        sideMenuOverlay.classList.remove("visible");
        closeButton.style.display = "none";
        searchButton.style.display = "block";
    }
});


const categoryButtons = document.querySelectorAll(".category-side-menu button");
const menuPages = document.querySelectorAll(".page-menu");

const chemin = window.location.pathname;

let pageActive = 0;

if (chemin.startsWith("/film")) {
    pageActive = 1;
} else if (chemin.startsWith("/serie")) {
    pageActive = 2;
} else if (chemin.startsWith("/anime")) {
    pageActive = 0;
}

menuPages.forEach((page, index) => {
    page.style.display = index === pageActive ? "flex" : "none";
});

categoryButtons[pageActive].classList.add("active");

categoryButtons.forEach((button, index) => {
    button.addEventListener("click", () => {
        menuPages.forEach(page => {
            page.style.display = "none";
        });

        categoryButtons.forEach(button => {
            button.classList.remove("active");
        });

        menuPages[index].querySelector(".media-search").value = "";
        menuPages[index].style.display = "flex";
        button.classList.add("active");
    });
});

// recherche anime
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