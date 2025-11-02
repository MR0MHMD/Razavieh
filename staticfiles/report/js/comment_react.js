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
                    if (!data.success) {
                        if (data.error === 'login_required') {
                            alert("برای ثبت واکنش باید وارد حساب کاربری شوید.");
                        }
                        return;
                    }

                    // ✅ بروزرسانی شمارنده‌ها
                    commentCard.querySelector('.like-count').textContent = data.likes;
                    commentCard.querySelector('.dislike-count').textContent = data.dislikes;

                    // ✅ دکمه‌ها
                    const likeImg = commentCard.querySelector('.reaction-btn[data-reaction="like"] img');
                    const dislikeImg = commentCard.querySelector('.reaction-btn[data-reaction="dislike"] img');

                    // بازگرداندن آیکون‌ها به حالت عادی
                    likeImg.src = '/static/report/icons/like.svg';
                    dislikeImg.src = '/static/report/icons/dislike.svg';

                    // اگر واکنش فعال است، آیکون مربوطه را تغییر بده
                    if (data.user_reaction === 'like') {
                        likeImg.src = '/static/report/icons/selected_like.svg';
                    } else if (data.user_reaction === 'dislike') {
                        dislikeImg.src = '/static/report/icons/selected_dislike.svg';
                    }
                })
                .catch(error => console.error('Error:', error));
        });
    });

    // گرفتن csrf token از کوکی‌ها
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