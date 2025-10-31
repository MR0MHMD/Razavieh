
document.addEventListener("DOMContentLoaded", () => {
  const slides = document.querySelectorAll(".hero-image img");
  if (slides.length === 0) return;
  let index = 0;

  slides[index].classList.add("active");
  setInterval(() => {
    slides[index].classList.remove("active");
    index = (index + 1) % slides.length;
    slides[index].classList.add("active");
  }, 5000);
});