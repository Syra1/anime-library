let series = [];

const serieList = document.getElementById("serie-list");

const unknownOriginalTitle = "Titre original inconnu";

loadMedia("/serie/api", (medias) => {

    series = medias;

}, serieList, "serie", "series", unknownOriginalTitle);


function animerSerieAjoute(serieId) {

    const selector = `.serie-card[data-serie-id="${serieId}"]`;

    const card = document.querySelector(selector);

    if (!card) {
        return;
    }

    card.classList.add("magic-card");

}