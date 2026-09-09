const saisons = document.querySelectorAll(".season-item-media-detail input[type='checkbox']");

saisons.forEach((saison) => {
    saison.addEventListener("change", () => {
        modifierSaisonVue(
            saison.dataset.typeMedia,
            saison.dataset.mediaId,
            saison.dataset.saisonId,
            saison.checked
        );
    });
});

async function modifierSaisonVue(typeMedia, mediaId, saisonId, vu) {
    await fetch(
        `/${typeMedia}/${mediaId}/saison/${saisonId}/vu?vu=${vu}`,
        {
            method: "POST"
        }
    );
}