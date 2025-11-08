document.addEventListener("DOMContentLoaded", () => {
    const openBtn = document.getElementById("openCategoryModal");
    const closeBtn = document.getElementById("closeCategoryModal");
    const modal = document.getElementById("categoryModal");

    if (openBtn && modal) {
        openBtn.addEventListener("click", () => modal.classList.add("active"));
    }

    if (closeBtn) {
        closeBtn.addEventListener("click", () => modal.classList.remove("active"));
    }

    modal?.addEventListener("click", (e) => {
        if (e.target.classList.contains("category-modal-backdrop")) {
            modal.classList.remove("active");
        }
    });
});
