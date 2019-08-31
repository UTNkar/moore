function marvin(message, classes, callback) {
    var marvin_style = 'rounded';
    if(classes !== '') {
        marvin_style += ' ' + classes;
    }

    Materialize.toast(
        '<div class="message-impl">' +
        // TODO: Replace this static reference.
        '<img class="marvin" src="/static/images/bocken_white.svg">' +
        '<b>Bocken:</b><a href="#" class="close"><i class="material-icons">close</i></a><br>'
        + message
        + '</div>',
        Infinity, // Display until dismissed
        marvin_style,
        callback
    );

    $('.message-impl > .close').click(function(ev){
        ev.preventDefault();
        $(this).closest('.toast')[0].M_Toast.remove();
    });
}

$(document).ready(function() {
    $('.message').each(function(index, value) {
        var classes = '';
        if ($(value).hasClass('error')) {
            classes = 'red';
        } else if ($(value).hasClass('warning')) {
            classes = 'yellow black-text';
        }
        marvin($(this).text(), classes, null);
    });
});
