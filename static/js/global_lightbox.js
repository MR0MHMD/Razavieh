document.addEventListener("DOMContentLoaded", () => {
    const box = document.getElementById("global-lightbox");
    const backdrop = box.querySelector(".lb-backdrop");
    const img = box.querySelector(".lightbox-img");
    const closeBtn = box.querySelector(".lb-close");
    const nextBtn = box.querySelector(".next");
    const prevBtn = box.querySelector(".prev");
    const dlBtn = box.querySelector(".lb-download");
    const counter = box.querySelector(".lb-counter");

    // selectors to gather possible images (robust)
    const selectors = [
        ".lightbox-item",
        ".report-gallery .gallery-item img",
        ".poster-image-box img",
        ".post-image",
        ".notification-card img",
        ".post-card img",
        ".report-thumb img",
        "img" // fallback - careful: may include all imgs
    ];

    // collect image nodes once (call refreshImages() if DOM updates)
    let images = []; // {el, src, group}
    function refreshImages() {
        images = [];
        const seen = new Set();
        selectors.forEach(sel => {
            document.querySelectorAll(sel).forEach(el => {
                // skip if invisible or very small or already added
                if (!(el instanceof HTMLImageElement)) return;
                const src = el.getAttribute("src") || el.dataset.src || "";
                if (!src) return;
                if (seen.has(el)) return;
                seen.add(el);

                // prefer explicit class 'lightbox-item' to include all, otherwise only images with data-lightbox="1"
                // but to be safe we include elements that are inside report/post/notification containers
                const group = el.dataset.group || el.closest('[data-lightbox-group]')?.dataset?.lightboxGroup || el.closest('.report')?.dataset?.id || "default";
                images.push({el, src, group});
            });
        });
    }

    refreshImages();

    // utility: build map of groups to arrays
    function groupsMap() {
        const map = new Map();
        images.forEach(it => {
            if (!map.has(it.group)) map.set(it.group, []);
            map.get(it.group).push(it);
        });
        // preserve document order inside each group
        return map;
    }

    let currentGroup = null;
    let groupImages = [];
    let currentIndex = 0;

    // zoom handling
    let zoom = 1;
    let panX = 0, panY = 0;

    function applyTransform() {
        img.style.transform = `scale(${zoom}) translate(${panX}px, ${panY}px)`;
    }

    function resetZoom() {
        zoom = 1;
        panX = panY = 0;
        applyTransform();
    }

    // show image by index in groupImages
    function showImageAt(i) {
        if (!groupImages.length) return;
        currentIndex = (i + groupImages.length) % groupImages.length;
        const data = groupImages[currentIndex];
        // set src
        img.src = data.src;
        counter.textContent = `${currentIndex + 1} / ${groupImages.length}`;
        resetZoom();
        // hide nav if single
        const single = groupImages.length <= 1;
        nextBtn.style.display = single ? "none" : "flex";
        prevBtn.style.display = single ? "none" : "flex";
    }

    function openByElement(el) {
        refreshImages(); // refresh in case new images added
        // find index in images
        const idx = images.findIndex(i => i.el === el);
        if (idx === -1) return;
        const group = images[idx].group;
        currentGroup = group;
        groupImages = images.filter(it => it.group === group);
        // ensure groupImages keep the same order as in images
        showImageAt(groupImages.findIndex(g => g.el === el));
        box.classList.add("active");
        box.setAttribute("aria-hidden", "false");
        document.body.style.overflow = "hidden";
    }

    // open when clicking any image that matches our selectors
    document.addEventListener("click", (e) => {
        let target = e.target;
        if (target.tagName === "IMG") {
            // prefer if element has class lightbox-item or data-group or is inside recognized container
            const ok = target.classList.contains("lightbox-item") || target.closest('.report') || target.closest('.notification') || target.closest('.post') || target.closest('.report-gallery') || target.closest('.poster-image-box') || target.closest('.post-image-wrapper');
            if (!ok) return;
            e.preventDefault();
            openByElement(target);
        }
    });

    function close() {
        box.classList.remove("active");
        box.setAttribute("aria-hidden", "true");
        document.body.style.overflow = "";
        resetZoom();
    }

    closeBtn.addEventListener("click", close);
    backdrop.addEventListener("click", close);
    // close with Escape
    document.addEventListener("keydown", (e) => {
        if (!box.classList.contains("active")) return;
        if (e.key === "Escape") close();
        if (e.key === "ArrowRight") next();
        if (e.key === "ArrowLeft") prev();
    });

    // navigation
    function next() {
        if (!groupImages.length || groupImages.length === 1) return;
        showImageAt(currentIndex + 1);
    }

    function prev() {
        if (!groupImages.length || groupImages.length === 1) return;
        showImageAt(currentIndex - 1);
    }

    nextBtn.addEventListener("click", (e) => {
        e.stopPropagation();
        next();
    });
    prevBtn.addEventListener("click", (e) => {
        e.stopPropagation();
        prev();
    });

    // download
    dlBtn.addEventListener("click", (e) => {
        e.stopPropagation();
        if (!groupImages.length) return;
        const a = document.createElement("a");
        a.href = groupImages[currentIndex].src;
        a.download = groupImages[currentIndex].src.split('/').pop() || "image";
        document.body.appendChild(a);
        a.click();
        a.remove();
    });

    // DOUBLE TAP / DOUBLE CLICK to zoom at point
    let lastClick = 0;
    img.addEventListener("click", (e) => {
        const now = Date.now();

        if (now - lastClick < 250) {     // double tap detected
            const rect = img.getBoundingClientRect();
            const clickX = e.clientX - rect.left;
            const clickY = e.clientY - rect.top;

            if (zoom === 1) {
                zoom = 2.4;

                // موقعیت دقیق برای اینکه نقطه کلیک شده مرکز زوم شود
                const centerX = rect.width / 2;
                const centerY = rect.height / 2;

                const diffX = centerX - clickX;
                const diffY = centerY - clickY;

                // تبدیل اختلاف‌ها به مقدار جابجایی پان
                panX = diffX / 1.4;
                panY = diffY / 1.4;

            } else {
                resetZoom();
            }

            applyTransform();
        }

        lastClick = now;
    });

    // TOUCH SWIPE left/right and drag-to-close
    let touchStartX = 0, touchStartY = 0, touchStartTime = 0;
    let draggingDown = false;

    box.addEventListener("touchstart", (ev) => {
        if (!ev.changedTouches || !ev.changedTouches[0]) return;
        touchStartX = ev.changedTouches[0].clientX;
        touchStartY = ev.changedTouches[0].clientY;
        touchStartTime = Date.now();
        draggingDown = false;
    }, {passive: true});

    box.addEventListener("touchmove", (ev) => {
        if (!ev.changedTouches || !ev.changedTouches[0]) return;
        const dx = ev.changedTouches[0].clientX - touchStartX;
        const dy = ev.changedTouches[0].clientY - touchStartY;

        // if vertical drag more than horizontal and downward, perform drag-to-close visual
        if (Math.abs(dy) > Math.abs(dx) && dy > 10 && Math.abs(dy) > 30) {
            draggingDown = true;
            // apply a translateY to lb-inner (via img transform)
            const t = dy / 2; // damping
            box.querySelector('.lb-inner').style.transform = `translateY(${t}px)`;
            box.style.background = `rgba(0,0,0,${Math.max(0.15, 0.65 - Math.abs(dy) / 500)})`;
        }
    }, {passive: true});

    box.addEventListener("touchend", (ev) => {
        if (!ev.changedTouches || !ev.changedTouches[0]) return;
        const dx = ev.changedTouches[0].clientX - touchStartX;
        const dy = ev.changedTouches[0].clientY - touchStartY;
        const dt = Date.now() - touchStartTime;

        // vertical swipe down to close threshold
        if (draggingDown && dy > 120) {
            // animate out
            box.querySelector('.lb-inner').style.transition = 'transform .25s ease';
            box.querySelector('.lb-inner').style.transform = `translateY(120%)`;
            setTimeout(() => {
                box.querySelector('.lb-inner').style.transition = '';
                box.querySelector('.lb-inner').style.transform = '';
                box.style.background = '';
                close();
            }, 260);
            return;
        } else {
            // reset visual
            box.querySelector('.lb-inner').style.transition = 'transform .18s ease';
            box.querySelector('.lb-inner').style.transform = '';
            box.style.background = '';
            setTimeout(() => {
                box.querySelector('.lb-inner').style.transition = '';
            }, 220);
        }

        // horizontal swipe for next/prev (fast enough or enough distance)
        if (Math.abs(dx) > Math.max(40, window.innerWidth * 0.08)) {
            if (dx < 0) next();
            else prev();
            return;
        }

        // click with touch handled by click/dbltap logic above
    }, {passive: true});

    // mouse wheel to next/prev
    img.addEventListener("wheel", (e) => {
        if (!box.classList.contains("active")) return;
        if (Math.abs(e.deltaX) > Math.abs(e.deltaY)) {
            if (e.deltaX > 0) next(); else prev();
        }
    });

    // expose refresh function (optional)
    window.myLightbox = {
        refresh: refreshImages,
        openElement: openByElement
    };
});