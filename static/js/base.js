document.addEventListener("DOMContentLoaded", () => {
    const menuToggle = document.getElementById("menuToggle");
    const navMenu = document.querySelector(".nav-menu");

    menuToggle.addEventListener("click", () => {
        navMenu.classList.toggle("active");
        menuToggle.classList.toggle("open");
        menuToggle.innerHTML = menuToggle.classList.contains("open")
            ? '<i class="fas fa-times"></i>'
            : '<i class="fas fa-bars"></i>';
    });
});

document.addEventListener("DOMContentLoaded", () => {
    const icons = document.querySelectorAll(".social-icons img");

    function updateIconsForTheme(theme) {
        icons.forEach(icon => {
            const lightSrc = icon.getAttribute("data-light");
            const darkSrc = icon.getAttribute("data-dark");

            if (theme === "dark") {
                icon.src = darkSrc;
            } else {
                icon.src = lightSrc;
            }
        });
    }

    // اگر سایتت با data-theme روی body کار می‌کنه:
    const observer = new MutationObserver(() => {
        const theme = document.body.getAttribute("data-theme") || "light";
        updateIconsForTheme(theme);
    });

    observer.observe(document.body, {attributes: true, attributeFilter: ["data-theme"]});

    // اجرای اولیه هنگام بارگذاری صفحه
    const initialTheme = document.body.getAttribute("data-theme") || "light";
    updateIconsForTheme(initialTheme);
});

<!-- ✅ Service Worker Registration -->

if ('serviceWorker' in navigator) {
    window.addEventListener('load', function () {
        navigator.serviceWorker.register("{% static 'main/js/service-worker.js' %}")
            .then(function (registration) {
                console.log('Service Worker registered with scope:', registration.scope);
            })
            .catch(function (error) {
                console.log('Service Worker registration failed:', error);
            });
    });
}
document.addEventListener("DOMContentLoaded", () => {
    const loader = document.getElementById("page-loader");
    if (!loader) return;

    const minDisplayTime = 750;
    const startTime = performance.now();

    window.addEventListener("load", () => {
        const elapsed = performance.now() - startTime;
        const remaining = Math.max(0, minDisplayTime - elapsed);
        setTimeout(() => {
            loader.classList.add("hidden");
            setTimeout(() => loader.remove(), 800);
        }, remaining);
    });
});
