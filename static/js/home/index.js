document.addEventListener("DOMContentLoaded", () => {

    const INTERVALLE_CARROUSEL = 2; // temps du defilement en secondes
    const carrousel = document.querySelector(".watch-category");

    if (!carrousel) return;

    const cards = [...carrousel.querySelectorAll(".watch-item")];

    if (cards.length <= 6) return;

    const nombreCards = cards.length;

    carrousel.style.setProperty("justify-content", "flex-start");

    /*
     * On crée 2 copies :
     *
     * [ ORIGINAL ][ COPIE ][ COPIE ]
     *
     * On démarre dans la copie du milieu.
     */
    cards.forEach(card => {
        carrousel.appendChild(card.cloneNode(true));
    });

    cards.forEach(card => {
        carrousel.appendChild(card.cloneNode(true));
    });

    let toutesLesCards = [
        ...carrousel.querySelectorAll(".watch-item")
    ];

    /*
     * Fonction permettant de centrer une card.
     */
    function centrerCard(card, smooth = false) {

        const position =
            card.offsetLeft
            - (carrousel.clientWidth - card.offsetWidth) / 2;

        carrousel.scrollTo({
            left: position,
            behavior: smooth ? "smooth" : "auto"
        });
    }

    /*
     * On commence dans le groupe du milieu.
     *
     * +3 permet de ne pas commencer exactement
     * au bord du groupe.
     */
    let index = nombreCards + 3;

    centrerCard(toutesLesCards[index]);

    /*
     * Déplacement automatique.
     */
    function prochaineCard() {

        index++;

        /*
         * On déplace normalement.
         */
        centrerCard(toutesLesCards[index], true);

        /*
         * Lorsque l'on arrive dans le troisième groupe,
         * on revient dans le deuxième groupe.
         */
        if (index >= nombreCards * 2) {

            setTimeout(() => {

                index -= nombreCards;

                /*
                 * On désactive temporairement le scroll smooth.
                 */
                carrousel.style.scrollBehavior = "auto";

                centrerCard(toutesLesCards[index], false);

                /*
                 * On force le navigateur à appliquer
                 * immédiatement la nouvelle position.
                 */
                carrousel.offsetHeight;

                /*
                 * On remet le comportement smooth.
                 */
                carrousel.style.scrollBehavior = "smooth";

            }, 700);
        }
    }

    setInterval(prochaineCard, INTERVALLE_CARROUSEL * 1000);

});