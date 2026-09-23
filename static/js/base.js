
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

categoryButtons.forEach((button, index) => {
    button.addEventListener("click", () => {
        menuPages.forEach(page => {
            page.style.display = "none";
        });

        menuPages[index].style.display = "flex";
    });
});

// recherche anime
const animeSideSearch = document.querySelector("#anime-side-search");

let animes = [];

fetch("/anime/api")
    .then(response => response.json())
    .then(resultats => {
        animes = resultats;
    });

animeSideSearch.addEventListener("input", () => {
    const recherche = animeSideSearch.value.trim();

    if (recherche.length < 3) {
        return;
    }

    const rechercheNormalisee = recherche
        .normalize("NFD")
        .replace(/[\u0300-\u036f]/g, "")
        .toLowerCase()
        .trim();

    const resultats = animes.filter(anime => {
        const titre = anime.titre
            .normalize("NFD")
            .replace(/[\u0300-\u036f]/g, "")
            .toLowerCase();

        const titreOriginal = anime.titre_original
            .normalize("NFD")
            .replace(/[\u0300-\u036f]/g, "")
            .toLowerCase();

        return (
            titre.includes(rechercheNormalisee) ||
            titreOriginal.includes(rechercheNormalisee)
        );
    });

const searchResults = document.querySelector("#anime-search-results");

searchResults.innerHTML = resultats.map(anime => `
    <a href="/anime/${anime.id}" class="search-result">

        <img
            class="search-result-image"
            src="${anime.image || ""}"
            alt="${anime.titre}"
        >

        <div class="search-result-info">

            <p>${anime.titre || "Titre inconnu"}</p>

            <p>${anime.titre_original || "Titre original inconnu"}</p>

            ${anime.annee ? `<p>${anime.annee}</p>` : ""}

        </div>

    </a>
`).join("");

});