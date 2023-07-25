function messageAlert() {
    const message = document.querySelector('#message-alert-id')
    message.style.display = 'flex'
    setTimeout(function() {
        message.style.display = 'none'
    }, 5000)
}