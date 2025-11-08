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
                    if (!data || data.redirect) return;
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
    toast.className = "toast";
    document.body.appendChild(toast);
    setTimeout(() => toast.classList.add('show'), 100);
    setTimeout(() => toast.remove(), 1500);
}