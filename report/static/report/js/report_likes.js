document.addEventListener('DOMContentLoaded', () => {
  document.querySelectorAll('.like-btn').forEach(button => {
    button.addEventListener('click', () => {
      const reportId = button.dataset.id;

      fetch(`/report/like/${reportId}/`)
        .then(response => {
          if (response.status === 401) {
            return response.json().then(data => {
              showToast(data.message);
              setTimeout(() => window.location.href = data.redirect, 1800);
            });
          }
          return response.json();
        })
        .then(data => {
          if (!data || data.redirect) return; // از مرحله قبلی برگشته
          const icon = button.querySelector('img');
          const countEl = button.parentElement.querySelector('.like-count');

          countEl.textContent = data.likes_count;
          icon.src = data.liked
            ? "/static/report/icons/heart_full.svg"
            : "/static/report/icons/heart_empty.svg";
        })
        .catch(err => console.error(err));
    });
  });
});

function showToast(message) {
  const toast = document.createElement('div');
  toast.textContent = message;
  toast.style.position = 'fixed';
  toast.style.bottom = '20px';
  toast.style.left = '50%';
  toast.style.transform = 'translateX(-50%)';
  toast.style.background = '#333';
  toast.style.color = '#fff';
  toast.style.padding = '10px 20px';
  toast.style.borderRadius = '10px';
  toast.style.zIndex = '9999';
  toast.style.opacity = '0';
  toast.style.transition = 'opacity 0.3s ease';
  document.body.appendChild(toast);
  setTimeout(() => (toast.style.opacity = '1'), 100);
  setTimeout(() => toast.remove(), 1500);
}