document.addEventListener("DOMContentLoaded", () => {
    const wrapper = document.querySelector(".report-media-wrapper");
    if (!wrapper) return;

    const reportId = wrapper.dataset.reportId;
    const reportSlug = wrapper.dataset.reportSlug;
    const contentEl = document.getElementById("media-content");
    const tabs = wrapper.querySelectorAll(".media-tab");

    if (!contentEl || !tabs.length) return;

    /* -----------------------------
       build ajax url
    ----------------------------- */
    const buildUrl = (media) =>
        `/report/report_detail/${reportId}/${reportSlug}/media/${media}/`;

    /* -----------------------------
       fade helpers
    ----------------------------- */
    const fadeOut = (el, cb) => {
        el.style.transition = "opacity 200ms ease, transform 200ms ease";
        el.style.opacity = 0;
        el.style.transform = "translateY(6px)";
        setTimeout(() => cb && cb(), 210);
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

    /* -----------------------------
       after ajax load hooks
       (هیچ منطق صوت / ویدیو اینجا نیست)
    ----------------------------- */
    function afterLoad() {
        // فقط hook
        if (window.myLightbox && typeof window.myLightbox.refresh === "function") {
            window.myLightbox.refresh();
        }

        if (typeof window.initAudioPlayers === "function") {
            window.initAudioPlayers();
        }
    }

    /* -----------------------------
       tab click logic
    ----------------------------- */
    tabs.forEach(tab => {
        tab.addEventListener("click", () => {
            if (tab.classList.contains("active")) return;

            const media = tab.dataset.media;
            if (!media) return;

            // update active state
            tabs.forEach(t => {
                t.classList.remove("active");
                t.setAttribute("aria-selected", "false");
            });

            tab.classList.add("active");
            tab.setAttribute("aria-selected", "true");

            const url = buildUrl(media);

            fadeOut(contentEl, () => {
                fetch(url, {
                    method: "GET",
                    headers: {"X-Requested-With": "XMLHttpRequest"}
                })
                    .then(resp => {
                        if (resp.status === 204) return "";
                        if (!resp.ok) throw new Error("fetch failed");
                        return resp.text();
                    })
                    .then(html => {
                        contentEl.innerHTML =
                            html ||
                            `<div class="card">
                                <p class="text-muted">هیچ محتوایی موجود نیست.</p>
                             </div>`;

                        setTimeout(() => {
                            fadeIn(contentEl);
                            afterLoad();
                        }, 10);
                    })
                    .catch(() => {
                        contentEl.innerHTML = `
                            <div class="card">
                                <p class="text-muted">
                                    خطا در بارگذاری. دوباره تلاش کنید.
                                </p>
                            </div>`;
                        fadeIn(contentEl);
                    });
            });
        });
    });

    // init for default loaded tab
    afterLoad();
});