document.addEventListener("DOMContentLoaded", () => {
    const modal = document.getElementById("donationModal");
    const backdrop = document.getElementById("donationBackdrop");
    const closeBtn = document.getElementById("donationModalClose");
    const copyCardBtn = document.getElementById("copyCardBtn");
    const copyShebaBtn = document.getElementById("copyShebaBtn");
    const openLinkBtn = document.getElementById("openLinkBtn");
    const modalCardEl = document.getElementById("modalCard");
    const modalShebaEl = document.getElementById("modalSheba");
    const modalTitle = document.getElementById("modalTitle");
    const toast = document.getElementById("modalToast");

    let activeCard = null;
    let activeSheba = null;
    let activeLink = null;
    let activeTitle = null;
    let toastTimer = null;

    function showModal(card, sheba, link, title) {
        activeCard = card || "";
        activeSheba = sheba || "";
        activeLink = link || "";
        activeTitle = title || "انتخاب عملیات";

        modalCardEl.textContent = activeCard || "تعریف نشده";
        modalShebaEl.textContent = activeSheba || "تعریف نشده";
        modalTitle.textContent = title;

        // disable link button if no link
        if (!activeLink) {
            openLinkBtn.setAttribute("disabled", "disabled");
            openLinkBtn.style.opacity = "0.6";
            openLinkBtn.title = "لینک پرداخت تعریف نشده است";
        } else {
            openLinkBtn.removeAttribute("disabled");
            openLinkBtn.style.opacity = "1";
            openLinkBtn.title = "";
        }

        modal.classList.add("active");
        modal.setAttribute("aria-hidden", "false");
    }

    function hideModal() {
        modal.classList.remove("active");
        modal.setAttribute("aria-hidden", "true");
    }

    function showToast(message) {
        if (toastTimer) clearTimeout(toastTimer);
        toast.textContent = message;
        toast.classList.add("show");
        toastTimer = setTimeout(() => {
            toast.classList.remove("show");
        }, 1800);
    }

    // Attach click to each card
    document.querySelectorAll(".donation-card").forEach(el => {
        el.addEventListener("click", () => {
            const card = el.dataset.card?.trim() || "";
            const sheba = el.dataset.sheba?.trim() || "";
            const link = el.dataset.link?.trim() || "";
            const title = el.querySelector(".donation-title")?.textContent?.trim() || "عملیات کارت";

            showModal(card, sheba, link, title);
        });
    });

    // backdrop or close btn hides modal
    backdrop?.addEventListener("click", hideModal);
    closeBtn?.addEventListener("click", hideModal);

    // helper copy (uses clipboard API with fallback)
    async function copyToClipboard(text) {
        if (!text) {
            showToast("مقداری برای کپی وجود ندارد");
            return false;
        }
        try {
            if (navigator.clipboard && navigator.clipboard.writeText) {
                await navigator.clipboard.writeText(text);
            } else {
                // fallback
                const ta = document.createElement("textarea");
                ta.value = text;
                ta.style.position = "fixed";
                ta.style.left = "-9999px";
                document.body.appendChild(ta);
                ta.select();
                document.execCommand("copy");
                document.body.removeChild(ta);
            }
            return true;
        } catch (err) {
            console.error("copy failed", err);
            return false;
        }
    }

    copyCardBtn?.addEventListener("click", async () => {
        const ok = await copyToClipboard(activeCard);
        if (ok) showToast("✅ شماره کارت کپی شد");
        else showToast("❌ کپی انجام نشد");
    });

    copyShebaBtn?.addEventListener("click", async () => {
        const ok = await copyToClipboard(activeSheba);
        if (ok) showToast("✅ شماره شبا کپی شد");
        else showToast("❌ کپی انجام نشد");
    });

    openLinkBtn?.addEventListener("click", () => {
        if (!activeLink) {
            showToast("لینک پرداخت تعریف نشده است");
            return;
        }
        // باز کردن در تب جدید
        window.open(activeLink, "_blank", "noopener");
        showToast("در حال باز کردن درگاه...");
    });

    // close on Escape
    document.addEventListener("keydown", (e) => {
        if (e.key === "Escape") hideModal();
    });
});