
let currentSlide = 0;
let sliderInterval;

function showSlide(index) {
    const slides = document.querySelectorAll(".hero-slide");
    const dots = document.querySelectorAll(".slider-dot");

    if (!slides.length) return;

    currentSlide = (index + slides.length) % slides.length;

    slides.forEach((slide, i) => {
        slide.classList.toggle("active", i === currentSlide);
    });

    dots.forEach((dot, i) => {
        dot.classList.toggle("active", i === currentSlide);
    });
}

function changeSlide(direction) {
    showSlide(currentSlide + direction);
    restartSlider();
}

function goToSlide(index) {
    showSlide(index);
    restartSlider();
}

function startSlider() {
    clearInterval(sliderInterval);

    sliderInterval = setInterval(() => {
        showSlide(currentSlide + 1);
    }, 4000);
}

function restartSlider() {
    startSlider();
}

document.addEventListener("DOMContentLoaded", () => {
    showSlide(0);
    startSlider();
});
