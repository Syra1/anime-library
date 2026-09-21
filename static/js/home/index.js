document.addEventListener("DOMContentLoaded", () => {

    const INTERVALLE_CARROUSEL = 6; // en secondes

    const carrousel = document.querySelector(".watch-category");

    if (!carrousel) return;

    const cards = [...carrousel.querySelectorAll(".watch-item")];

    if (cards.length <= 6) return;

    const nombreCards = cards.length;

    carrousel.style.setProperty("justify-content", "flex-start");

    cards.forEach(card => {
        carrousel.appendChild(card.cloneNode(true));
    });

    cards.forEach(card => {
        carrousel.appendChild(card.cloneNode(true));
    });

    const toutesLesCards = [
        ...carrousel.querySelectorAll(".watch-item")
    ];

    function centrerCard(card, smooth = false) {

        const position =
            card.offsetLeft
            - (carrousel.clientWidth - card.offsetWidth) / 2;

        carrousel.scrollTo({
            left: position,
            behavior: smooth ? "smooth" : "auto"
        });
    }

    let index = nombreCards + 3;

    centrerCard(toutesLesCards[index]);

    function enleverEffet() {

        toutesLesCards.forEach(card => {
            card.classList.remove("active");
        });
    }

function prochaineCard() {

    enleverEffet();

    index++;

    centrerCard(toutesLesCards[index], true);

    if (index >= nombreCards * 2) {

        setTimeout(() => {

            index -= nombreCards;

            carrousel.style.scrollBehavior = "auto";

            centrerCard(toutesLesCards[index], false);

            carrousel.offsetHeight;

            carrousel.style.scrollBehavior = "smooth";

            toutesLesCards[index].classList.add("active");

        }, 1000);

    } else {

        setTimeout(() => {

            toutesLesCards[index].classList.add("active");

        }, 1000);

    }
}

    setInterval(
        prochaineCard,
        INTERVALLE_CARROUSEL * 1000
    );

});