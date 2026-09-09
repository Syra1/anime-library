let searchTimeout = null;
const minimumSearchLength = 3;
const mediaAnimationDelay = 100;

function normalizeText(text) {
    return (text || "")
        .normalize("NFD")
        .replace(/[\u0300-\u036f]/g, "")
        .toLowerCase()
        .trim();
}

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
        searchResults.innerHTML = `<p> Impossible d'effectuer la recherche. </p>`;
    }
}

function handleMediaSearch(searchInput, searchResults, searchUrl, displaySearchResults, searchDelay) {
    const recherche = searchInput.value.trim();
    clearTimeout(searchTimeout);
    const rechercheTropCourte = recherche.length < minimumSearchLength;
    if (rechercheTropCourte) {
        searchResults.innerHTML = "";
        return;
    }
    searchTimeout = setTimeout(
        () => {
            searchTMDB(recherche, searchUrl, searchResults, displaySearchResults);
        }, searchDelay);
}

async function loadMedia(url, setMedia, mediaList, typeMedia, mediaName, unknownOriginalTitle) {
    try {
        const response = await fetch(url);
        if (!response.ok) {
            throw new Error(`Erreur lors du chargement des ${mediaName}`);
        }
        const resultats = await response.json();
        const medias = Array.isArray(resultats) ? resultats : [];
        setMedia(medias);
        displayMedia(medias, "", mediaList, typeMedia, unknownOriginalTitle);
    } catch (error) {
        console.error(`Erreur chargement ${mediaName} :`, error);
        mediaList.innerHTML = `<p> Impossible de charger les ${mediaName}. </p>`;
    }
}

function createMediaCard(media, typeMedia, unknownOriginalTitle) {
    const titre = media.titre || "Titre inconnu";
    const titreOriginal = media.titre_original || unknownOriginalTitle;
    const image = media.image;
    const mediaId = media.id;
    return `
        <div class="media-card-background">

            <a href="/${typeMedia}/${mediaId}" class="${typeMedia}-card media-card" data-${typeMedia}-id="${mediaId}">
                <div class="media-image">
                    <img src="${image || ""}" alt="${titre}">
                </div>
                <div class="media-info">
                    <h2>
                        ${titre}
                    </h2>
                    <p class="original-title">
                        ${titreOriginal}
                    </p>
                </div>
            </a>
        </div>
    `;
}

function displayMedia(medias, search, mediaList, typeMedia, unknownOriginalTitle) {
    const recherche = normalizeText(search);
    const filteredMedias = medias.filter((media) => {
        const titre = normalizeText(media.titre);
        const titreOriginal = normalizeText(media.titre_original);
        return (titre.includes(recherche) || titreOriginal.includes(recherche));
    });

    if (filteredMedias.length === 0) {
        mediaList.innerHTML = `<p>Aucun média trouvé.</p>`;
        return;
    }
    const mediaCards = filteredMedias.map((media) => createMediaCard(media, typeMedia, unknownOriginalTitle)).join("");
    mediaList.innerHTML = mediaCards;
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
                    <h3> ${titre} </h3>
                    <p> ${titreOriginal} </p>
                    ${ annee ? `<p> ${annee} </p>`: ""}
                </div>
                <button class="add-${typeMedia}-button add-media-button" data-tmdb-id="${tmdbId}">
                    Ajouter
                </button>
            </article>
        `;
    }).join("");
    const searchResultsHTML = `<div class="search-results-list"> ${searchResultsList} </div>`;
    searchResults.innerHTML = searchResultsHTML;
    const addMediaButtons = document.querySelectorAll(`.add-${typeMedia}-button`);
    addMediaButtons.forEach(button => {
        button.addEventListener("click", addMedia);
    });
}

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
        await loadMedia(loadUrl, setMedia, mediaList, typeMedia, mediaName, unknownOriginalTitle);
        const mediaId = resultat[`${typeMedia}_id`];
        setTimeout(() => {
            animateMedia(mediaId);
        }, mediaAnimationDelay);
        button.textContent = "Ajouté";
    } catch (error) {
        console.error(`Erreur ajout ${mediaName} :`, error);
        alert(`Erreur pendant l'ajout du ${mediaName}.`);
        button.disabled = false;
        button.textContent = "Ajouter";
    }
}

function handleDocumentClick(event, mediaSearch, searchResults, librarySearch, displayMedias) {
    const clicDansRecherche = mediaSearch.contains(event.target);
    const clicDansResultats = searchResults.contains(event.target);
    const clicDansLibrarySearch = librarySearch.contains(event.target);
    const clicEnDehorsRecherche = !clicDansRecherche && !clicDansResultats;
    const clicEnDehorsRechercheBibliotheque = !clicDansLibrarySearch;
    if (clicEnDehorsRecherche) {
        mediaSearch.value = "";
        searchResults.innerHTML = "";
    }
    if (clicEnDehorsRechercheBibliotheque) {
        if (librarySearch.value !== "") {
            librarySearch.value = "";
            displayMedias("");
        }
    }
}