document.addEventListener("DOMContentLoaded", () => {
    const realFileInput = document.querySelector('input[type="file"]');
    const label = document.createElement("label");
    const wrapper = document.createElement("div");
    const fileName = document.createElement("span");

    wrapper.className = "file-upload-wrapper";
    label.className = "file-upload-label";
    label.innerHTML = '<i class="fas fa-upload"></i> انتخاب فایل';
    fileName.className = "file-name";
    fileName.textContent = "هیچ فایلی انتخاب نشده است";

    realFileInput.parentNode.insertBefore(wrapper, realFileInput);
    wrapper.appendChild(label);
    wrapper.appendChild(realFileInput);
    wrapper.appendChild(fileName);

    label.addEventListener("click", () => realFileInput.click());

    realFileInput.addEventListener("change", () => {
        if (realFileInput.files.length > 1) {
            fileName.textContent = `${realFileInput.files.length} فایل انتخاب شد`;
        } else if (realFileInput.files.length === 1) {
            fileName.textContent = realFileInput.files[0].name;
        } else {
            fileName.textContent = "هیچ فایلی انتخاب نشده است";
        }
    });
});
