let searchTimeout = null;
const minimumSearchLength = 3;

function normalizeText(text) {

    return (text || "")
        .normalize("NFD")
        .replace(/[\u0300-\u036f]/g, "")
        .toLowerCase()
        .trim();
}

async function searchTMDB(
    recherche,
    url,
    searchResults,
    displaySearchResults
) {
    searchResults.innerHTML = `
        <p>Recherche en cours...</p>
    `;

    try {
        const encodedRecherche =
            encodeURIComponent(recherche);

        const response =
            await fetch(
                `${url}?q=${encodedRecherche}`
            );

        if (!response.ok) {
            throw new Error(
                "Erreur lors de la recherche"
            );
        }

        const resultats =
            await response.json();

        displaySearchResults(resultats);

    } catch (error) {
        console.error(
            "Erreur recherche TMDB :",
            error
        );

        searchResults.innerHTML = `
            <p>
                Impossible d'effectuer la recherche.
            </p>
        `;
    }
}

function handleMediaSearch(
    searchInput,
    searchResults,
    searchUrl,
    displaySearchResults,
    searchDelay
) {
    const recherche =
        searchInput.value.trim();

    clearTimeout(
        searchTimeout
    );

    const rechercheTropCourte =
        recherche.length <
        minimumSearchLength;

    if (rechercheTropCourte) {
        searchResults.innerHTML = "";
        return;
    }

    searchTimeout =
        setTimeout(
            () => {
                searchTMDB(
                    recherche,
                    searchUrl,
                    searchResults,
                    displaySearchResults
                );
            },
            searchDelay
        );
}

async function loadMedia(
    url,
    setMedia,
    mediaList,
    typeMedia,
    mediaName,
    unknownOriginalTitle
) {

    try {

        const response =
            await fetch(url);

        if (!response.ok) {

            throw new Error(
                `Erreur lors du chargement des ${mediaName}`
            );

        }

        const resultats =
            await response.json();

        const medias =
            Array.isArray(resultats)
                ? resultats
                : [];

        setMedia(medias);

        displayMedia(
            medias,
            "",
            mediaList,
            typeMedia,
            unknownOriginalTitle
        );

    } catch (error) {

        console.error(
            `Erreur chargement ${mediaName} :`,
            error
        );

        mediaList.innerHTML = `
            <p>
                Impossible de charger les ${mediaName}.
            </p>
        `;
    }
}

function createMediaCard(
    media,
    typeMedia,
    unknownOriginalTitle
) {

    const titre =
        media.titre || "Titre inconnu";

    const titreOriginal =
        media.titre_original ||
        unknownOriginalTitle;

    const image =
        media.image;

    const mediaId =
        media.id;

    return `
        <div class="media-card-background">

            <a
                href="/${typeMedia}/${mediaId}"
                class="${typeMedia}-card media-card"
                data-${typeMedia}-id="${mediaId}"
            >

                <div class="media-image">

                    <img
                        src="${image || ""}"
                        alt="${titre}"
                    >

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

function displayMedia(
    medias,
    search,
    mediaList,
    typeMedia,
    unknownOriginalTitle
) {

    const recherche =
        normalizeText(search);

    const filteredMedias =
        medias.filter(
            (media) => {

                const titre =
                    normalizeText(
                        media.titre
                    );

                const titreOriginal =
                    normalizeText(
                        media.titre_original
                    );

                return (
                    titre.includes(recherche) ||
                    titreOriginal.includes(recherche)
                );
            }
        );

    if (filteredMedias.length === 0) {

        mediaList.innerHTML = `
            <p>Aucun média trouvé.</p>
        `;

        return;
    }

    const mediaCards =
        filteredMedias
            .map(
                (media) =>
                    createMediaCard(
                        media,
                        typeMedia,
                        unknownOriginalTitle
                    )
            )
            .join("");

    mediaList.innerHTML =
        mediaCards;
}