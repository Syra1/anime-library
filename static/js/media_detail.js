const saisons = document.querySelectorAll(".season-item-media-detail input[type='checkbox']");

saisons.forEach((saison, index) => {
    saison.addEventListener("change", () => {

        const saisonsIds = [];

        if (saison.checked) {
            // Coche toutes les saisons précédentes.
            for (let i = 0; i <= index; i++) {
                saisons[i].checked = true;
                saisonsIds.push(
                    saisons[i].dataset.saisonId
                );
            }
        } else {
            // Décoche toutes les saisons suivantes.
            for (let i = index; i < saisons.length; i++) {
                saisons[i].checked = false;
                saisonsIds.push(
                    saisons[i].dataset.saisonId
                );
            }
        }

        modifierSaisonVue(
            saison.dataset.typeMedia,
            saison.dataset.mediaId,
            saisonsIds,
            saison.checked
        );
    });
});


async function modifierSaisonVue(
    typeMedia,
    mediaId,
    saisonsIds,
    vu
) {
    await fetch(
        `/${typeMedia}/${mediaId}/saisons/vu?vu=${vu}`,
        {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(saisonsIds)
        }
    );
}