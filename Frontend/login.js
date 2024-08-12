document.getElementById('email').addEventListener('input', function () {
    const btnSend = document.getElementById('btn-send');
    if (this.value.length > 0) {
        btnSend.classList.add('button-moved');
    } else {
        btnSend.classList.remove('button-moved');
    }
});
