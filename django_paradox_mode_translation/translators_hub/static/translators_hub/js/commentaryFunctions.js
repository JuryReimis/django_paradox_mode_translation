
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
            $('#likes-comment-' + commentId).text(response.likes)
            $('#dislikes-comment-' + commentId).text(response.dislikes)
            $('#like-button-' + commentId).removeClass(response.remove_like_class).addClass(response.add_like_class)
            $('#dislike-button-' + commentId).removeClass(response.remove_dis_class).addClass(response.add_dis_class)
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
            $('#likes-comment-' + commentId).text(response.likes)
            $('#dislikes-comment-' + commentId).text(response.dislikes)
            $('#like-button-' + commentId).removeClass(response.remove_like_class).addClass(response.add_like_class)
            $('#dislike-button-' + commentId).removeClass(response.remove_dis_class).addClass(response.add_dis_class)
        },
        error: function (error) {
            console.log('Ошибка при отправке запроса: ', error);
        }
    });
}