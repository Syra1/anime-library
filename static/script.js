let animes = [];
let currentFilter = "all";


async function loadAnimes() {
    try {
        const response = await fetch("/animes");

        if (!response.ok) {
            throw new Error("Erreur lors du chargement des animés");
        }

        animes = await response.json();

        displayAnimes();

    } catch (error) {
        console.error(error);

        document.getElementById("anime-list").innerHTML = `
            <p>Impossible de charger les animés.</p>
        `;
    }
}


function displayAnimes() {
    const searchInput = document.getElementById("search");
    const search = searchInput.value.toLowerCase();

    const animeList = document.getElementById("anime-list");

    const filteredAnimes = animes.filter(anime => {

        const matchesSearch =
            anime.titre.toLowerCase().includes(search) ||
            (
                anime.titre_original &&
                anime.titre_original.toLowerCase().includes(search)
            );


        const matchesFilter =
            currentFilter === "all" ||
            (currentFilter === "watched" && anime.vu) ||
            (currentFilter === "unwatched" && !anime.vu);


        return matchesSearch && matchesFilter;
    });


    if (filteredAnimes.length === 0) {
        animeList.innerHTML = `
            <p>Aucun anime trouvé.</p>
        `;

        return;
    }


    animeList.innerHTML = filteredAnimes.map(anime => {

        const statusClass = anime.vu
            ? "watched"
            : "unwatched";

        const statusText = anime.vu
            ? "✓ Vu"
            : "○ Non vu";


        return `
            <article class="anime-card">

                <h2>${anime.titre}</h2>

                <p class="original-title">
                    ${anime.titre_original || "Titre original inconnu"}
                </p>

                <p class="status ${statusClass}">
                    ${statusText}
                </p>

            </article>
        `;

    }).join("");
}


document
    .getElementById("search")
    .addEventListener("input", displayAnimes);


document
    .querySelectorAll(".filter")
    .forEach(button => {

        button.addEventListener("click", () => {

            document
                .querySelectorAll(".filter")
                .forEach(button => {
                    button.classList.remove("active");
                });


            button.classList.add("active");

            currentFilter = button.dataset.filter;

            displayAnimes();
        });
    });


loadAnimes();
