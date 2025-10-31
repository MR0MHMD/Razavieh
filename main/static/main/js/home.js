// دکمه تغییر تم
const toggle = document.createElement('button');
toggle.textContent = "🌓 تغییر تم";
toggle.classList.add('theme-toggle');
document.body.appendChild(toggle);

// بررسی تم ذخیره‌شده در localStorage
if (localStorage.getItem('theme') === 'dark') {
  document.body.setAttribute('data-theme', 'dark');
} else {
  document.body.setAttribute('data-theme', 'light');
}

// تغییر تم با کلیک
toggle.addEventListener('click', () => {
  const current = document.body.getAttribute('data-theme');
  const newTheme = current === 'dark' ? 'light' : 'dark';
  document.body.setAttribute('data-theme', newTheme);
  localStorage.setItem('theme', newTheme);
});

// افکت پارالاکس برای تصویر
document.addEventListener("scroll", () => {
  const heroImage = document.querySelector(".hero-image img.active");
  if (!heroImage) return;
  const scrollPos = window.scrollY;
  const offset = scrollPos * 0.15; // سرعت پارالاکس
  heroImage.style.transform = `translateY(${offset}px) scale(1.05)`;
});

// اسلایدر خودکار تصاویر هیرو
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