// static/report/js/report_media_tabs.js
document.addEventListener("DOMContentLoaded", () => {
    const wrapper = document.querySelector(".report-media-wrapper");
    if (!wrapper) return;

    const reportId = wrapper.dataset.reportId;
    const reportSlug = wrapper.dataset.reportSlug;
    const contentEl = document.getElementById("media-content");
    const tabs = wrapper.querySelectorAll(".media-tab");

    // helper: build url
    const buildUrl = (media) => `/report/report_detail/${reportId}/${reportSlug}/media/${media}/`;

    // fade helper
    const fadeOut = (el, cb) => {
        el.style.transition = "opacity 200ms ease, transform 200ms ease";
        el.style.opacity = 0;
        el.style.transform = "translateY(6px)";
        setTimeout(() => {
            cb && cb();
        }, 210);
    };
    const fadeIn = (el) => {
        el.style.opacity = 0;
        el.style.transform = "translateY(6px)";
        requestAnimationFrame(() => {
            el.style.transition = "opacity 260ms ease, transform 260ms ease";
            el.style.opacity = 1;
            el.style.transform = "translateY(0)";
        });
    };

    // Re-init functions: باید بعد از بارگذاری partial ها اجرا بشن
    function initAfterLoad() {
        // ویدیوها: bind click
        initVideoCards();
        // lightbox تصاویر: existing global_lightbox.js binds document click,
        // اما اگر نیاز به refresh داشته باشی می‌تونی window.myLightbox.refresh()
        if (window.myLightbox && typeof window.myLightbox.refresh === 'function') {
            window.myLightbox.refresh();
        }
    }

    // attach click handlers for tabs
    tabs.forEach(tab => {
        tab.addEventListener("click", (e) => {
            const media = tab.dataset.media;
            // ignore if already active
            if (tab.classList.contains("active")) return;

            // update active class & aria
            tabs.forEach(t => {
                t.classList.remove("active");
                t.setAttribute("aria-selected", "false");
            });
            tab.classList.add("active");
            tab.setAttribute("aria-selected", "true");

            // fetch partial
            const url = buildUrl(media);

            // gracefully handle empty result
            fadeOut(contentEl, () => {
                fetch(url, {method: "GET", headers: {"X-Requested-With": "XMLHttpRequest"}})
                    .then(resp => {
                        if (resp.status === 204) return ""; // no content
                        if (!resp.ok) throw new Error("خطا در دریافت داده‌ها");
                        return resp.text();
                    })
                    .then(html => {
                        contentEl.innerHTML = html || `<div class="card"><p class="text-muted">هیچ محتوایی موجود نیست.</p></div>`;
                        // small delay then fadeIn
                        setTimeout(() => {
                            fadeIn(contentEl);
                            initAfterLoad();
                        }, 10);
                    })
                    .catch(err => {
                        console.error(err);
                        contentEl.innerHTML = `<div class="card"><p class="text-muted">خطا در بارگذاری. دوباره تلاش کنید.</p></div>`;
                        fadeIn(contentEl);
                    });
            });
        });
    });

    // initial init (in case default content already present)
    initAfterLoad();

    // ----------------------------
    // Video cards init (re-usable)
    // ----------------------------
    function initVideoCards() {
        const cards = document.querySelectorAll(".video-card");
        const lightbox = document.getElementById("videoLightbox");
        const iframe = document.getElementById("videoPlayer");

        // remove previous listeners by cloning nodes (simple cleanup)
        // but careful: don't break other bindings; we'll rebind on each card
        cards.forEach(card => {
            // avoid attaching duplicate handlers
            if (card.dataset._bound === "1") return;
            card.dataset._bound = "1";

            card.addEventListener("click", () => {
                const url = card.dataset.player;
                if (!iframe) return;
                iframe.src = url;
                if (lightbox) {
                    lightbox.style.display = "flex";
                    document.body.style.overflow = "hidden";
                }
            });
        });

        // close logic
        const closeBtn = document.querySelector(".video-close");

        function closeVideo() {
            if (iframe) iframe.src = "";
            if (lightbox) {
                lightbox.style.display = "none";
                document.body.style.overflow = "";
            }
        }

        if (closeBtn && !closeBtn.dataset._videoCloseBound) {
            closeBtn.addEventListener("click", closeVideo);
            closeBtn.dataset._videoCloseBound = "1";
        }

        if (lightbox && !lightbox.dataset._videoLightboxBound) {
            lightbox.addEventListener("click", (e) => {
                if (e.target === lightbox) closeVideo();
            });
            document.addEventListener("keydown", (e) => {
                if (e.key === "Escape") closeVideo();
            });
            lightbox.dataset._videoLightboxBound = "1";
        }
    }
});