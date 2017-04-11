$(document).ready(function() {
    $('.message').each(function( index ) {
        Materialize.toast(
            '<div class="message-impl">' +
            // TODO: Replace this static reference.
            '<img class="marvin" src="/static/images/marvin.png">' +
            '<b>Marvin:</b><br>'
            + $(this).text()
            + '</div>');
    });
});