const saisons = document.querySelectorAll(".season-item-media-detail input[type='checkbox']");

saisons.forEach((saison, index) => {
    saison.addEventListener("change", () => {

        if (saison.checked) {
            // Coche toutes les saisons précédentes.
            for (let i = 0; i < index; i++) {
                if (!saisons[i].checked) {
                    saisons[i].checked = true;

                    modifierSaisonVue(
                        saisons[i].dataset.typeMedia,
                        saisons[i].dataset.mediaId,
                        saisons[i].dataset.saisonId,
                        true
                    );
                }
            }
        } else {
            // Décoche toutes les saisons suivantes.
            for (let i = index + 1; i < saisons.length; i++) {
                if (saisons[i].checked) {
                    saisons[i].checked = false;

                    modifierSaisonVue(
                        saisons[i].dataset.typeMedia,
                        saisons[i].dataset.mediaId,
                        saisons[i].dataset.saisonId,
                        false
                    );
                }
            }
        }

        // Enregistre la saison actuellement cliquée.
        modifierSaisonVue(
            saison.dataset.typeMedia,
            saison.dataset.mediaId,
            saison.dataset.saisonId,
            saison.checked
        );
    });
});


async function modifierSaisonVue(
    typeMedia,
    mediaId,
    saisonId,
    vu
) {
    await fetch(
        `/${typeMedia}/${mediaId}/saison/${saisonId}/vu?vu=${vu}`,
        {
            method: "POST"
        }
    );
}