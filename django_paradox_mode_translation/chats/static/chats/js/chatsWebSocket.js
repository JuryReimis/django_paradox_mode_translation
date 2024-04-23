// chat_url = document.getElementById('chat').value

function handshake(chatUrl) {
    let socket = new WebSocket('ws://' + window.location.host + '/' + 'ws/' + 'chats/' + chatUrl + '/')
    console.log(chatUrl)

    socket.onmessage = function (e) {

        let data = JSON.parse(e.data);
        let message = data.body;
        let author = data.author;
        let pub_date = data.pub_date
        let chatMessages = $('#' + chatUrl + '-chat-messages');
        chatMessages.append((`<p><p>${pub_date}</p><b>${author}:</b> ${message}</p>`))
    }

    let openButton = $('#open-button-' + chatUrl)
    openButton.click(function () {
        scrollToPosition(4, chatUrl)
    })

    let form = $('#chat-form-' + chatUrl)

    form.submit(function (e) {
        const csrfToken = Cookies.get('csrftoken')
        e.preventDefault()
        const full_url = 'http://' + window.location.host + '/' + 'chats/' + chatUrl + '/'

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
