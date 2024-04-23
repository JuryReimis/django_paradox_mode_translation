// chat_url = document.getElementById('chat').value

function handshake(chat_url) {
    let socket = new WebSocket('ws://' + window.location.host + '/' + 'ws/' + 'chats/' + chat_url + '/')
    console.log(chat_url)

    socket.onmessage = function (e) {

        let data = JSON.parse(e.data);
        let message = data.body;
        let author = data.author;
        let pub_date = data.pub_date
        let chatMessages = $('#' + chat_url + '-chat-messages');
        chatMessages.append((`<p><p>${pub_date}</p><b>${author}:</b> ${message}</p>`))
    }

    let form = $('#chat-form-' + chat_url)

    form.submit(function (e) {
        const csrfToken = Cookies.get('csrftoken')
        e.preventDefault()
        const full_url = 'http://' + window.location.host + '/' + 'chats/' + chat_url + '/'

        $.ajax({
            url: full_url,
            method: "POST",
            headers: {
                'X-CSRFToken': csrfToken
            },
            data: $(e.target).serialize(),
            success: function (response) {
                console.log('response - ok')
                $(e.target).trigger('reset')
            },

            error: function (error) {
                console.log('Ошибка', error)
            }
        })
    })
}
