const mobileSearchBtn = document.getElementById("mobileSearchBtn");
    const mobileSearchPopup = document.getElementById("mobileSearchPopup");

    // باز و بسته شدن با کلیک روی دکمه
    mobileSearchBtn?.addEventListener("click", (e) => {
        e.stopPropagation();
        mobileSearchPopup.classList.toggle("active");
    });

    // بستن با کلیک بیرون از باکس
    document.addEventListener("click", (e) => {
        if (!mobileSearchPopup.contains(e.target) && !mobileSearchBtn.contains(e.target)) {
            mobileSearchPopup.classList.remove("active");
        }
    });
    document.querySelectorAll(".has-submenu").forEach(link => {
        link.addEventListener("click", function (e) {
            const submenu = this.nextElementSibling;
            const isOpen = submenu.classList.contains("active");

            // بستن بقیه زیرمنوها
            document.querySelectorAll(".submenu-content.active").forEach(openMenu => {
                openMenu.classList.remove("active");
            });

            // باز یا بسته کردن همین یکی
            if (!isOpen) submenu.classList.add("active");

            // جلوگیری از لینک شدن خود دکمه
            e.preventDefault();
        });
    });
    document.addEventListener("DOMContentLoaded", () => {
  const searchBtn = document.querySelector(".search-btn");
  const searchInput = document.querySelector(".search-input");

  searchBtn.addEventListener("click", (e) => {
    // اگر باز نشده بود، فقط بازش کن (جستجو نکن)
    if (!searchInput.classList.contains("active")) {
      e.preventDefault();
      searchInput.classList.add("active");
      searchInput.focus();
    }
  });

  // اگر کاربر بیرون کلیک کرد، ببندش
  document.addEventListener("click", (e) => {
    if (!e.target.closest(".search-bar-wrapper")) {
      searchInput.classList.remove("active");
    }
  });
});