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
                    <div class="titres-media">
                        <h1>
                            ${titre}
                        </h1>
                        <h2>
                            (${titreOriginal})
                        </h2>
                    </div>
                    ${media.auteur ? `
                        <p class="auteur-media">
                            ${media.auteur}
                        </p>
                    ` : ""}
                    ${media.suivi ? `
                        <p class="saisons-media">
                            <img src="/static/icons/Eye.svg" alt="Vu">
                            ${media.suivi.vus}/${media.suivi.total} saisons
                        </p>
                    ` : ""}
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