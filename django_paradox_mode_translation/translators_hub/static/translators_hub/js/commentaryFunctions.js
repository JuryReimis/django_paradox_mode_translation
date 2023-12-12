
function likeComment(commentId) {
    // Отправить AJAX-запрос на сервер для увеличения счетчика лайков
    const element = document.getElementById('likes-comment-' + commentId)
    const url = element.getAttribute('data-url')
    const pageData = element.getAttribute('data-page')
    const csrfToken = Cookies.get('csrftoken')
    $.ajax({
        url: url,
        method: 'POST',
        headers: {'X-CSRFToken': csrfToken},
        data: {
            'page_data': pageData,
            'comment_pk': commentId,
        },
        success: function (response) {
            // Обновить отображение счетчика лайков на странице
            element.textContent = response.likes
        },
        error: function (error) {
            console.log('Ошибка при отправке запроса: ', error);
        }
    });
}

function dislikeComment(commentId) {
    // Отправить AJAX-запрос на сервер для увеличения счетчика дизлайков
    const element = document.getElementById('dislikes-comment-' + commentId)
    const url = element.getAttribute('data-url')
    const pageData = element.getAttribute('data-page')
    const csrfToken = Cookies.get('csrftoken')
    $.ajax({
        url: url,
        method: 'POST',
        headers: {'X-CSRFToken': csrfToken},
        data: {
            'page_data': pageData,
            'comment_pk': commentId,
        },
        success: function (response) {
            // Обновить отображение счетчика дизлайков на странице
            element.textContent = response.dislikes;
        },
        error: function (error) {
            console.log('Ошибка при отправке запроса: ', error);
        }
    });
}