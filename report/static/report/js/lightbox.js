document.addEventListener("DOMContentLoaded", () => {
    const lightbox = document.getElementById("lightbox");
    const lightboxImg = lightbox.querySelector(".lightbox-img");
    const closeBtn = lightbox.querySelector(".close");
    const nextBtn = lightbox.querySelector(".next");
    const prevBtn = lightbox.querySelector(".prev");

    const images = Array.from(document.querySelectorAll(".report-gallery .gallery-item img"));
    let currentIndex = 0;

    function openLightbox(index) {
        currentIndex = index;
        lightboxImg.src = images[index].getAttribute("src");
        lightbox.classList.add("active");
        document.body.style.overflow = "hidden"; // جلوگیری از اسکرول پس‌زمینه
    }

    function closeLightbox() {
        lightbox.classList.remove("active");
        document.body.style.overflow = "";
    }

    function showNext() {
        currentIndex = (currentIndex + 1) % images.length;
        lightboxImg.src = images[currentIndex].getAttribute("src");
    }

    function showPrev() {
        currentIndex = (currentIndex - 1 + images.length) % images.length;
        lightboxImg.src = images[currentIndex].getAttribute("src");
    }

    images.forEach((img, index) => {
        img.style.cursor = "pointer";
        img.addEventListener("click", () => openLightbox(index));
    });

    closeBtn.addEventListener("click", closeLightbox);
    nextBtn.addEventListener("click", (e) => {
        e.stopPropagation();
        showNext();
    });
    prevBtn.addEventListener("click", (e) => {
        e.stopPropagation();
        showPrev();
    });

    lightbox.addEventListener("click", (e) => {
        if (e.target === lightbox) closeLightbox();
    });

    document.addEventListener("keydown", (e) => {
        if (!lightbox.classList.contains("active")) return;
        if (e.key === "ArrowRight") showNext();
        if (e.key === "ArrowLeft") showPrev();
        if (e.key === "Escape") closeLightbox();
    });
});