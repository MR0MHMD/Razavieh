(function () {

    function formatTime(sec) {
        if (!sec || isNaN(sec)) return "00:00";
        const m = Math.floor(sec / 60).toString().padStart(2, "0");
        const s = Math.floor(sec % 60).toString().padStart(2, "0");
        return `${m}:${s}`;
    }

    window.initAudioPlayers = function () {

        document.querySelectorAll(".audio-player").forEach(player => {

            // جلوگیری از bind دوباره
            if (player.dataset.bound === "1") return;
            player.dataset.bound = "1";

            const src = player.dataset.src;
            if (!src) return;

            const playBtn = player.querySelector(".ap-play");
            const downloadBtn = player.querySelector(".ap-download");
            const timeline = player.querySelector(".ap-timeline");
            const progress = player.querySelector(".ap-progress");
            const currentEl = player.querySelector(".ap-current");
            const totalEl = player.querySelector(".ap-total");

            const audio = new Audio(src);
            audio.preload = "metadata";

            /* ---------- metadata ---------- */
            audio.addEventListener("loadedmetadata", () => {
                totalEl.textContent = formatTime(audio.duration);
            });

            /* ---------- progress ---------- */
            audio.addEventListener("timeupdate", () => {
                if (!audio.duration) return;
                currentEl.textContent = formatTime(audio.currentTime);
                progress.style.width = (audio.currentTime / audio.duration) * 100 + "%";
            });

            audio.addEventListener("ended", () => {
                playBtn.classList.remove("ap-playing");
            });

            /* ---------- play / pause ---------- */
            playBtn.addEventListener("click", (e) => {
                e.stopPropagation();

                if (audio.paused) {
                    audio.play();
                    playBtn.classList.add("ap-playing");
                } else {
                    audio.pause();
                    playBtn.classList.remove("ap-playing");
                }
            });

            /* ---------- seek (RTL safe) ---------- */
            function seek(e) {
                const rect = timeline.getBoundingClientRect();

                let clientX = e.clientX;
                if (e.touches && e.touches.length) {
                    clientX = e.touches[0].clientX;
                }

                const isRTL = getComputedStyle(timeline).direction === "rtl";

                let percent;
                if (isRTL) {
                    percent = (rect.right - clientX) / rect.width;
                } else {
                    percent = (clientX - rect.left) / rect.width;
                }

                percent = Math.max(0, Math.min(1, percent));
                audio.currentTime = percent * audio.duration;
            }

            timeline.addEventListener("click", seek);
            timeline.addEventListener("touchstart", (e) => {
                e.preventDefault();
                seek(e);
            }, {passive: false});

            /* ---------- download ---------- */
            downloadBtn.addEventListener("click", (e) => {
                e.stopPropagation();

                const a = document.createElement("a");
                a.href = src;
                a.download = src.split("/").pop();
                document.body.appendChild(a);
                a.click();
                a.remove();
            });
        });
    };

    // برای لود اولیه صفحه (غیر AJAX)
    document.addEventListener("DOMContentLoaded", () => {
        if (typeof window.initAudioPlayers === "function") {
            window.initAudioPlayers();
        }
    });

})();