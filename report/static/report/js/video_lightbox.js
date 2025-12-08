document.addEventListener("DOMContentLoaded", () => {

    const lightbox = document.getElementById("videoLightbox");
    const iframe = document.getElementById("videoPlayer");
    const spinner = document.querySelector(".video-loading-spinner");
    const closeBtn = document.querySelector(".video-close-btn");

    let lightboxOpen = false;

    function openVideo(url) {

        // فقط وقتی pushState بزن که لایت‌باکس قبلاً باز نبوده
        if (!lightboxOpen) {
            window.history.pushState({videoLightbox: true}, "");
        }

        lightboxOpen = true;

        lightbox.style.display = "flex";
        spinner.style.display = "block";

        iframe.src = url;

        // قفل صفحه
        document.body.style.overflow = "hidden";
        document.body.style.touchAction = "none";
        document.body.style.position = "fixed";

        iframe.onload = () => {
            setTimeout(() => spinner.style.display = "none", 150);
        };
    }

    function closeVideo(triggerBack = false) {
        if (!lightboxOpen) return;

        lightboxOpen = false;

        iframe.src = "";
        spinner.style.display = "none";
        lightbox.style.display = "none";

        // آزادی صفحه
        document.body.style.overflow = "";
        document.body.style.touchAction = "auto";
        document.body.style.position = "";

        // اگه کاربر خودش بسته، باید یک بار back بزنیم
        if (triggerBack) {
            history.back();
        }
    }

    // کلیک روی کارت
    document.addEventListener("click", (e) => {
        const card = e.target.closest(".video-card");
        if (!card) return;

        openVideo(card.dataset.player);
    });

    // دکمه ضربدر
    closeBtn.addEventListener("click", () => closeVideo(true));

    // کلیک روی پس‌زمینه
    lightbox.addEventListener("click", (e) => {
        if (e.target.id === "videoLightbox") {
            closeVideo(true);
        }
    });

    // ESC
    document.addEventListener("keydown", (e) => {
        if (e.key === "Escape" && lightboxOpen) {
            closeVideo(true);
        }
    });

    // کنترل دکمه BACK مرورگر/موبایل
    window.addEventListener("popstate", (event) => {
        if (lightboxOpen) {
            closeVideo(false); // اینجا back نزنیم چون خود مرورگر زده
        }
    });

});