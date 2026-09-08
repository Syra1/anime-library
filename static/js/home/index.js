const carousels = document.querySelectorAll(".watch-category");

const speed = 75;

carousels.forEach((carousel) => {
    const duration = carousel.scrollWidth / speed;
    carousel.style.animationDuration = `${duration}s`;
});