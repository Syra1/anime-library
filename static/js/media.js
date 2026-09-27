const mediaAnimationDelay = 100;

async function loadMedia(url, setMedia, mediaList, typeMedia, mediaName, unknownOriginalTitle) {
    try {
        const response = await fetch(url);
        if (!response.ok) {
            throw new Error(`Erreur lors du chargement des ${mediaName}`);
        }
        const resultats = await response.json();
        const medias = Array.isArray(resultats) ? resultats : [];
        setMedia(medias);
        displayMedia(medias, mediaList, typeMedia, unknownOriginalTitle);
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
    const suivi = media.suivi
        ? `
            <p class="media-progress">
                ${media.suivi.vus} / ${media.suivi.total}
            </p>
        `
        : "";
    return `
        <div class="media-card-background">
            <a href="/${typeMedia}/${mediaId}" class="${typeMedia}-card media-card" data-${typeMedia}-id="${mediaId}">
                <div class="media-image">
                    <img src="${image || ""}" alt="${titre}">
                    ${suivi}
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

function displayMedia(medias, mediaList, typeMedia, unknownOriginalTitle) {

    if (medias.length === 0) {
        mediaList.innerHTML = `<p>Aucun média trouvé.</p>`;
        return;
    }

    const mediaCards = medias
        .map((media) => createMediaCard(media, typeMedia, unknownOriginalTitle))
        .join("");

    mediaList.innerHTML = mediaCards;
}

const watchButtons = document.querySelectorAll(".watch-button");

watchButtons.forEach((button) => {
    button.addEventListener("click", () => {
        const mediaType = button.id.replace("watch-button-", "");
        const watchList = document.querySelector(
            `#watch-list-${mediaType}`
        );

        if (!watchList) {
            return;
        }

        watchList.classList.toggle("visible");
    });
});