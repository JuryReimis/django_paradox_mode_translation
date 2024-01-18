

const user = document.getElementById('user-logged').value

console.log(user)
if (user !== 'AnonymousUser') {
    const socket = new WebSocket('ws://' + window.location.host +
    '/' +
    'ws/' +
    user +
    '/')

    socket.onmessage = function (event) {
        const element = document.getElementById('active-invites')
        $('#active-invites').text(JSON.parse(event.new_count))
    }



}


