document.addEventListener('DOMContentLoaded', function() {
    const reactionButtons = document.querySelectorAll('.reaction-btn');

    reactionButtons.forEach(button => {
        button.addEventListener('click', function() {
            const commentId = this.dataset.id;
            const reactionType = this.dataset.reaction;

            fetch('/report/react-comment/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCookie('csrftoken')
                },
                body: JSON.stringify({
                    comment_id: commentId,
                    reaction_type: reactionType
                })
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    const commentCard = button.closest('.comment-card');
                    commentCard.querySelector('.like-count').textContent = data.likes;
                    commentCard.querySelector('.dislike-count').textContent = data.dislikes;
                }
            })
            .catch(error => console.error('Error:', error));
        });
    });

    // تابع کمکی برای گرفتن CSRF
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
});