const carrousel = document.querySelector(".watch-category");
const cards = [...document.querySelectorAll(".watch-item")];

if (cards.length > 6) {

    const nombreCards = cards.length;

    // Copie des cards à la fin
    cards.forEach(card => {
        carrousel.appendChild(card.cloneNode(true));
    });

    // Copie des cards à la fin une deuxième fois
    cards.forEach(card => {
        carrousel.appendChild(card.cloneNode(true));
    });

    const toutesLesCards =
        [...carrousel.querySelectorAll(".watch-item")];

    // On commence au milieu
    let index = nombreCards + 3;

    toutesLesCards[index].scrollIntoView({
        behavior: "instant",
        block: "nearest",
        inline: "center"
    });

    function prochaineCard() {

        index++;

        toutesLesCards[index].scrollIntoView({
            behavior: "smooth",
            block: "nearest",
            inline: "center"
        });

        if (index >= nombreCards * 2) {

            carrousel.addEventListener("scrollend", function repositionner() {

                index -= nombreCards;

                const card = toutesLesCards[index];

                carrousel.scrollLeft =
                    card.offsetLeft -
                    (carrousel.clientWidth - card.offsetWidth) / 2;

                carrousel.removeEventListener(
                    "scrollend",
                    repositionner
                );

            });
        }
    }

    setInterval(prochaineCard, 5000);
}