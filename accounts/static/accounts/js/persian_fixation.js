function toEnglishDigits(str) {
    return str.replace(/[۰-۹]/g, d => "۰۱۲۳۴۵۶۷۸۹".indexOf(d))
        .replace(/[٠-٩]/g, d => "٠١٢٣٤٥٦٧٨٩".indexOf(d));
}

document.addEventListener("input", function (e) {
    if (e.target.classList.contains("persian-fix")) {
        e.target.value = toEnglishDigits(e.target.value);
    }
});