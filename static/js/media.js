const menuDeroulant = document.querySelector(".menu-deroulant-media");
const boutonMenu = document.querySelector(".menu-deroulant-bouton");
const optionsMenu = document.querySelectorAll(".menu-deroulant-options li");

optionsMenu[0].style.display = "none";

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
        optionsMenu.forEach((option) => {
            option.addEventListener("click", () => {
                const filtre = option.dataset.value;
                const mediasFiltres = filtrerMedias(medias, filtre);

                boutonMenu.querySelector("button").textContent = option.textContent;
                menuDeroulant.classList.remove("ouvert");

                optionsMenu.forEach((autreOption) => {
                    autreOption.style.display = "block";
                });

                option.style.display = "none";

                displayMedia(mediasFiltres, mediaList, typeMedia, unknownOriginalTitle);
            });
        });
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
                        <div class="saisons-media">
                            <img src="/static/icons/Eye.svg" alt="Vu">
                            ${media.suivi.total} saisons
                            <div class="suivis-media">
                                (${media.suivi.vus}/${media.suivi.total})
                            </div>
                        </div>
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

// Menu déroulant
boutonMenu.addEventListener("click", () => {
    menuDeroulant.classList.toggle("ouvert");
});

document.addEventListener("click", (event) => {
    if (!menuDeroulant.contains(event.target)) {
        menuDeroulant.classList.remove("ouvert");
    }
});

// Filtre menu déroulant 
function filtrerMedias(medias, filtre) {
    let mediasFiltres = [...medias];

    if (filtre === "vu") {
        mediasFiltres = mediasFiltres.filter(
            (media) =>
                !media.suivi ||
                media.suivi.vus === media.suivi.total
        );
    }

    if (filtre === "non-vu") {
        mediasFiltres = mediasFiltres.filter(
            (media) =>
                media.suivi &&
                media.suivi.vus !== media.suivi.total
        );
    }

    mediasFiltres.sort((a, b) =>
        a.titre.localeCompare(
            b.titre,
            "fr",
            { sensitivity: "base" }
        )
    );

    return mediasFiltres;
}