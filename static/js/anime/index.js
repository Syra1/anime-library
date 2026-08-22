// Déclaration des variables
let animes = [];
let currentAnimeToAdd = null;
let librarySearchTimeout = null;
let searchTimeout = null;
const addModal = document.getElementById("add-modal");
const seasonCountInput = document.getElementById("season-count");
const cancelAddButton = document.getElementById("cancel-add");
const confirmAddButton = document.getElementById("confirm-add");
const animeList = document.getElementById("anime-list");
const librarySearch = document.getElementById("search");
const animeSearch = document.getElementById("anime-search");
const searchResults = document.getElementById("search-results");
const minimumSearchLength = 3;
const librarySearchDelay = 500;
const animeSearchDelay = 300;
const animeAnimationDelay = 100;
const modalDisplay = "flex";
const modalHiddenDisplay = "none";
const unknownOriginalTitle = "Titre original inconnu";

// Charge les animés depuis la base de donnée.
async function loadAnimes() {
    try {
        const response = await fetch("/anime/api");
        if (!response.ok) {
            throw new Error("Erreur lors du chargement des animés");
        }
        const resultats = await response.json();
        animes = resultats;
        displayAnimes();
    } catch (error) {
        console.error(error);
        const message = `<p>Impossible de charger les animés.</p>`;
        animeList.innerHTML = message;
    }
}

// Normalise les noms pour la recherche, sans accents ni majuscules.
function normalizeText(text) {
    return (text || "")
        .normalize("NFD")
        .replace(/[\u0300-\u036f]/g, "")
        .toLowerCase();
}

// Filtre les animés, génère leurs cartes et les affiche dans la bibliothèque.
function displayAnimes(search = "") {
    const recherche = normalizeText(search);
    const filteredAnimes = animes.filter(anime => {
        const titre = normalizeText(anime.titre);
        const titre_original = normalizeText(anime.titre_original);
        return titre.includes(recherche) || titre_original.includes(recherche);
    });

    const aucunResultat = filteredAnimes.length === 0;
    if (aucunResultat) {
        const message = `<p>Aucun anime trouvé.</p>`;
        animeList.innerHTML = message;
        return;
    }
    const animeCards = filteredAnimes
        .map(anime => {
            const derniereSaisonVue = anime.saisons.reduce((max, saison) => {
                const saisonVue = saison.vue;
                const numeroSaison = saison.numero;
                if (saisonVue) {
                    return Math.max(max, numeroSaison);
                }
                return max;
            }, 0);

            const nombreSaisons = anime.saisons.length;
            const titre = anime.titre;
            const titreOriginal = anime.titre_original || unknownOriginalTitle;
            const image = anime.image;
            const animeId = anime.id;
            return `<a href="/anime/${animeId}" class="anime-card" data-anime-id="${animeId}">
                    <div class="anime-image">
                        <img src="${image}" alt="${titre}">
                        <span class="season-progress">
                            ${derniereSaisonVue} / ${nombreSaisons}
                        </span>
                    </div>
                    <div class="anime-info">
                        <h2>
                            ${titre}
                        </h2>
                        <p class="original-title">
                            ${titreOriginal}
                        </p>
                    </div>
                </a>`;
        })
        .join("");
    animeList.innerHTML = animeCards;
}

// Gère la saisie dans le champ de recherche de la bibliothèque.
function handleLibrarySearch() {
    clearTimeout(librarySearchTimeout);
    const recherche = librarySearch.value.trim();
    const rechercheTropCourte = recherche.length < minimumSearchLength;
    if (rechercheTropCourte) {
        displayAnimes("");
        return;
    }
    librarySearchTimeout = setTimeout(() => {
        displayAnimes(recherche);
    }, librarySearchDelay);
}

librarySearch.addEventListener("input", handleLibrarySearch);

// Gère la saisie dans le champ de recherche AniList.
function handleAnimeSearch() {
    const recherche = animeSearch.value.trim();
    clearTimeout(searchTimeout);
    const rechercheTropCourte = recherche.length < minimumSearchLength;
    if (rechercheTropCourte) {
        searchResults.innerHTML = "";
        return;
    }
    searchTimeout = setTimeout(() => {
        searchAniList(recherche);
    }, animeSearchDelay);
}

animeSearch.addEventListener("input", handleAnimeSearch);

// Recherche un anime via l'API AniList.
async function searchAniList(recherche) {
    const loadingMessage = `<p>Recherche en cours...</p>`;
    searchResults.innerHTML = loadingMessage;
    try {
        const encodedRecherche = encodeURIComponent(recherche);
        const url = "/anime/search-anime?q=" + encodedRecherche;
        const response = await fetch(url);
        if (!response.ok) {
            throw new Error("Erreur lors de la recherche");
        }
        const resultats = await response.json();
        displaySearchResults(resultats);
    } catch (error) {
        console.error(error);
        const errorMessage = `<p>Impossible de rechercher cet anime.</p>`;
        searchResults.innerHTML = errorMessage;
    }
}

// Affiche les résultats de la recherche via l'API AniList.
function displaySearchResults(resultats) {
    const aucunResultat = !resultats || resultats.length === 0;
    if (aucunResultat) {
        const message = `<p>Aucun anime trouvé.</p>`;
        searchResults.innerHTML = message;
        return;
    }
    const searchResultsList = resultats
        .map(anime => {
            const titreEnglish = anime.title.english;
            const titreRomaji = anime.title.romaji;
            const titrePrincipal = titreEnglish || titreRomaji;
            const titreSecondaire = titreRomaji;
            const image = anime.image;
            const anilistId = anime.id;
            return `<article class="search-result">
                    <img class="search-result-image" src="${image}" alt="${titrePrincipal}">
                    <div class="search-result-info">
                        <h3>
                            ${titrePrincipal}
                        </h3>
                        <p>
                            ${titreSecondaire}
                        </p>
                    </div>
                    <button class="add-anime-button" data-anilist-id="${anilistId}">
                        Ajouter
                    </button>
                </article>`;
        })
        .join("");
    const searchResultsHTML = `<div class="search-results-list">
        ${searchResultsList}
    </div>`;
    searchResults.innerHTML = searchResultsHTML;
    const addAnimeButtons = document.querySelectorAll(".add-anime-button");
    addAnimeButtons.forEach(button => {
        button.addEventListener("click", handleAddAnime);
    });
}

// Prépare l'ajout d'un anime
function handleAddAnime(event) {
    const button = event.currentTarget;
    const anilistId = Number(button.dataset.anilistId);
    currentAnimeToAdd = anilistId;
    seasonCountInput.value = 1;
    addModal.style.display = modalDisplay;
    seasonCountInput.focus();
    seasonCountInput.select();
}

// Ferme la fenêtre d'ajout et réinitialise l'anime sélectionné.
function handleCancelAdd() {
    addModal.style.display = modalHiddenDisplay;
    currentAnimeToAdd = null;
}

cancelAddButton.addEventListener("click", handleCancelAdd);

// Confirme l'ajout d'un anime et l'enregistre dans la base de donnée.
async function handleConfirmAdd() {
    const nombreSaisons = Number(seasonCountInput.value);
    const nombreSaisonsInvalide = !nombreSaisons || nombreSaisons < 1;
    if (nombreSaisonsInvalide) {
        alert("Nombre de saisons invalide.");
        return;
    }
    try {
        const url = "/anime/add-anime/" + currentAnimeToAdd;
        const requestOptions = {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({
                nombre_saisons: nombreSaisons,
            }),
        };
        const response = await fetch(url, requestOptions);
        const resultat = await response.json();
        const ajoutReussi = resultat.success;
        if (!ajoutReussi) {
            throw new Error();
        }
        addModal.style.display = modalHiddenDisplay;
        loadAnimes();
        const animeId = resultat.anime_id;
        setTimeout(() => {
            animerAnimeAjoute(animeId);
        }, animeAnimationDelay);
    } catch (error) {
        console.error(error);
        alert("Erreur pendant l'ajout.");
    }
}

confirmAddButton.addEventListener("click", handleConfirmAdd);

// Ferme les recherches lorsqu'un clic est effectué en dehors de la barre de recherche.
function handleDocumentClick(event) {
    const clicDansRecherche = animeSearch.contains(event.target);
    const clicDansResultats = searchResults.contains(event.target);
    const clicDansLibrarySearch = librarySearch.contains(event.target);
    const clicEnDehorsRechercheAnime = !clicDansRecherche && !clicDansResultats;
    const clicEnDehorsRechercheBibliotheque = !clicDansLibrarySearch;
    if (clicEnDehorsRechercheAnime) {
        animeSearch.value = "";
        searchResults.innerHTML = "";
    }
    if (clicEnDehorsRechercheBibliotheque) {
        librarySearch.value = "";
        displayAnimes("");
    }
}

document.addEventListener("click", handleDocumentClick);

// Gère les touches Entrée et Échap lorsque la fenêtre d'ajout est ouverte.
function handleDocumentKeydown(event) {
    const modalOuvert = addModal && addModal.style.display === modalDisplay;
    if (!modalOuvert) {
        return;
    }
    const toucheEntree = event.key === "Enter";
    const toucheEchap = event.key === "Escape";
    if (toucheEntree) {
        event.preventDefault();
        confirmAddButton.click();
    }
    if (toucheEchap) {
        event.preventDefault();
        cancelAddButton.click();
    }
}

document.addEventListener("keydown", handleDocumentKeydown);

// Prépare la nouvelle card pour l'animation CSS.
function animerAnimeAjoute(animeId) {
    const selector = `.anime-card[data-anime-id="${animeId}"]`;
    const card = document.querySelector(selector);
    if (!card) {
        return;
    }
    card.classList.add("magic-card");
}

// Recharge la liste des animés de la base de donnée.
loadAnimes();
