$(document).ready(function () {
    $('#chat-form').on('submit', function (e) {
        e.preventDefault();
        let humanInput = $('#human-input').val();
        if (humanInput.trim() !== '') {
            $('#chat-history').append(`<div class="chat-message human">${humanInput}</div>`);
            $('#human-input').val('');
            $.post('/chat', { human_input: humanInput }, function (data) {
                $('#chat-history').append(`<div class="chat-message ai">${data.response}</div>`);
                $('#chat-history').scrollTop($('#chat-history')[0].scrollHeight);
            });
        }
    });
});