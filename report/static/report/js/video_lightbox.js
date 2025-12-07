document.addEventListener("DOMContentLoaded", () => {

    const lightbox = document.getElementById("videoLightbox");
    const iframe = document.getElementById("videoPlayer");
    const spinner = document.querySelector(".video-loading-spinner");
    const closeBtn = document.querySelector(".video-close-btn");

    function openVideo(url) {
        lightbox.style.display = "flex";

        spinner.style.display = "block";

        iframe.src = url;

        iframe.onload = () => {
            setTimeout(() => {
                spinner.style.display = "none";
            }, 150);
        };
    }
    function closeVideo() {
        iframe.src = "";         // قطع پخش
        spinner.style.display = "none";
        lightbox.style.display = "none";
    }

    document.addEventListener("click", (e) => {
        const card = e.target.closest(".video-card");
        if (!card) return;

        const url = card.dataset.player;
        openVideo(url);
    });

    closeBtn.addEventListener("click", closeVideo);

    lightbox.addEventListener("click", (e) => {
        // فقط وقتی که دقیقاً روی پس‌زمینه زده شود
        if (e.target.id === "videoLightbox") {
            closeVideo();
        }
    });

    document.addEventListener("keydown", (e) => {
        if (e.key === "Escape") closeVideo();
    });
});