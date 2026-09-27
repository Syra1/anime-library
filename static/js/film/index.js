let films = [];

const filmList = document.getElementById("film-list");

const unknownOriginalTitle = "Titre original inconnu";

loadMedia("/film/api", (medias) => {

    films = medias;

}, filmList, "film", "films", unknownOriginalTitle);


function animerFilmAjoute(filmId) {

    const selector = `.film-card[data-film-id="${filmId}"]`;

    const card = document.querySelector(selector);

    if (!card) {
        return;
    }

    card.classList.add("magic-card");

}