function toast(message, classes, callback) {
    var toast_style = 'rounded';
    if(classes !== '') {
        toast_style += ' ' + classes;
	}
    Materialize.toast(
        '<div class="message-impl">' +
        // TODO: Replace this static reference.
        '<img class="bocken-toast" src="/static/images/bocken_white.png">' +
        '<b>Bocken:</b><a href="#" class="close"><i class="material-icons">close</i></a><br>'
        + message
        + '</div>',
        Infinity, // Display until dismissed
        toast_style,
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
        toast($(this).text(), classes, null);
    });
});