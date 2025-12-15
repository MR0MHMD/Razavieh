document.addEventListener('DOMContentLoaded', () => {
    const fileInput = document.querySelector('input[name="photo"]');
    const previewImg = document.getElementById('avatar-preview');
    const removeBtn = document.getElementById('remove-photo-btn');

    // 🔸 پیش‌نمایش تصویر
    if (fileInput) {
        fileInput.addEventListener('change', (e) => {
            const file = e.target.files[0];
            if (file) {
                const reader = new FileReader();
                reader.onload = (event) => {
                    previewImg.src = event.target.result;
                    previewImg.alt = "پیش‌نمایش تصویر جدید";
                };
                reader.readAsDataURL(file);
            }
        });
    }

    // 🔸 حذف عکس فعلی
    if (removeBtn) {
        removeBtn.addEventListener('click', () => {
            if (fileInput) fileInput.value = '';
            previewImg.src = "{% static 'profile-default.png' %}";
            previewImg.alt = "بدون تصویر";

            let removeInput = document.getElementById('remove_photo_field');
            if (!removeInput) {
                removeInput = document.createElement('input');
                removeInput.type = 'hidden';
                removeInput.name = 'remove_photo';
                removeInput.id = 'remove_photo_field';
                removeInput.value = '1';
                document.querySelector('form.edit-form').appendChild(removeInput);
            }
        });
    }
});