$(document).ready(function() {
    $('.message').each(function(index, value) {
        var classes = 'rounded';
        if ($(value).hasClass('error')) {
            classes += ' red';
        } else if ($(value).hasClass('warning')) {
            classes += ' yellow';
        }
        Materialize.toast(
            '<div class="message-impl">' +
            // TODO: Replace this static reference.
            '<img class="marvin" src="/static/images/marvin.png">' +
            '<b>Marvin:</b><br>'
            + $(this).text()
            + '</div>',
            null, // Display until dismissed
            classes
        );
    });
});