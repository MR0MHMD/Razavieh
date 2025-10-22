document.addEventListener('DOMContentLoaded', function () {
    const reactionButtons = document.querySelectorAll('.reaction-btn');

    reactionButtons.forEach(button => {
        button.addEventListener('click', function () {
            const commentId = this.dataset.id;
            const reactionType = this.dataset.reaction;
            const commentCard = this.closest('.comment-card');

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
                        commentCard.querySelector('.like-count').textContent = data.likes;
                        commentCard.querySelector('.dislike-count').textContent = data.dislikes;

                        const likeBtn = commentCard.querySelector('.reaction-btn[data-reaction="like"] img');
                        const dislikeBtn = commentCard.querySelector('.reaction-btn[data-reaction="dislike"] img');

                        // بازگرداندن آیکون‌ها به حالت عادی
                        likeBtn.src = '/static/report/icons/like.svg';
                        dislikeBtn.src = '/static/report/icons/dislike.svg';

                        // اگر واکنش جدیدی وجود داشت → تغییر آیکون
                        if (data.user_reaction === 'like') {
                            likeBtn.src = '/static/report/icons/selected_like.svg';
                        } else if (data.user_reaction === 'dislike') {
                            dislikeBtn.src = '/static/report/icons/selected_dislike.svg';
                        }
                    }
                })
                .catch(error => console.error('Error:', error));
        });
    });

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