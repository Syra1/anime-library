const searchButton = document.querySelector("#search-button");
const closeButton = document.querySelector("#close-button");
const sideMenu = document.querySelector("#side-menu");

searchButton.addEventListener("click", () => {
    sideMenu.classList.add("visible");
    searchButton.style.display = "none";
    closeButton.style.display = "block";
});

closeButton.addEventListener("click", () => {
    sideMenu.classList.remove("visible");
    closeButton.style.display = "none";
    searchButton.style.display = "block";
});