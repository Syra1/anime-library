const animeList = document.getElementById("anime-list");

const unknownOriginalTitle = "Titre original inconnu";

loadMedia("/anime/api", (medias) => {

    animes = medias;

}, animeList, "anime", "animes", unknownOriginalTitle);


function animerAnimeAjoute(animeId) {

    const selector = `.anime-card[data-anime-id="${animeId}"]`;

    const card = document.querySelector(selector);

    if (!card) {
        return;
    }

    card.classList.add("magic-card");

}