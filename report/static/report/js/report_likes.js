document.addEventListener('DOMContentLoaded', () => {
  document.querySelectorAll('.like-btn').forEach(button => {
    button.addEventListener('click', () => {
      const reportId = button.dataset.id;

      fetch(`/report/like/${reportId}/`)
        .then(response => response.json())
        .then(data => {
          const icon = button.querySelector('img');
          const countEl = button.parentElement.querySelector('.like-count');

          countEl.textContent = data.likes_count;

          if (data.liked) {
            icon.src = "/static/report/icons/heart_full.svg";
          } else {
            icon.src = "/static/report/icons/heart_empty.svg";
          }
        })
        .catch(err => console.error(err));
    });
  });
});