
document.addEventListener("DOMContentLoaded", () => {
  const slides = document.querySelectorAll(".hero-image img");
  if (slides.length === 0) return;
  let index = 0;

  slides[index].classList.add("active");
  setInterval(() => {
    slides[index].classList.remove("active");
    index = (index + 1) % slides.length;
    slides[index].classList.add("active");
  }, 5000);
});
let deferredPrompt;
const installBtn = document.getElementById('installBtn');

window.addEventListener('beforeinstallprompt', (e) => {
  e.preventDefault();
  deferredPrompt = e;
  installBtn.classList.add('show'); // دکمه رو نشون بده
});

installBtn.addEventListener('click', async () => {
  installBtn.classList.remove('show'); // مخفیش کن
  if (deferredPrompt) {
    deferredPrompt.prompt(); // پنجره نصب رو باز کن
    const choiceResult = await deferredPrompt.userChoice;
    if (choiceResult.outcome === 'accepted') {
      console.log('✅ نصب تایید شد');
    } else {
      console.log('❌ کاربر لغو کرد');
    }
    deferredPrompt = null;
  }
});

window.addEventListener('appinstalled', () => {
  console.log('🎉 اپلیکیشن نصب شد!');
  installBtn.style.display = 'none';
});