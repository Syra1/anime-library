const carousels = document.querySelectorAll(".watch-category");

const speed = 150;

carousels.forEach((carousel) => {
    const duration = carousel.scrollWidth / speed;
    carousel.style.animationDuration = `${duration}s`;
});