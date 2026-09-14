const carrousel = document.querySelector(".watch-category");
const cards = [...document.querySelectorAll(".watch-item")];

if (cards.length > 0) {

    // Crée une copie avant les cards originales
    cards.forEach(card => {
        const clone = card.cloneNode(true);
        carrousel.appendChild(clone);
    });

    // Crée une copie après les cards originales
    cards.forEach(card => {
        const clone = card.cloneNode(true);
        carrousel.appendChild(clone);
    });

    const toutesLesCards = [...carrousel.querySelectorAll(".watch-item")];
    const nombreCards = cards.length;

    // On commence sur la copie du milieu
    let index = nombreCards;

    // Place la 4e card au centre
    toutesLesCards[index + 3].scrollIntoView({
        behavior: "instant",
        block: "nearest",
        inline: "center"
    });

    index += 3;

    function prochaineCard() {

        index++;

        toutesLesCards[index].scrollIntoView({
            behavior: "smooth",
            block: "nearest",
            inline: "center"
        });

        // Si on arrive trop loin vers la droite
        if (index >= nombreCards * 2) {

            setTimeout(() => {

                index -= nombreCards;

                toutesLesCards[index].scrollIntoView({
                    behavior: "instant",
                    block: "nearest",
                    inline: "center"
                });

            }, 500);
        }
    }

    setInterval(prochaineCard, 4000);
}