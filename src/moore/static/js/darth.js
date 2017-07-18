$('document').ready(function() {
    $('body').append('<div id="toasty-darth"><img src="/static/libraries/misc/darth.png" alt="toasty"></div>');
    $('#toasty-darth').css('position', 'fixed');
    $('#toasty-darth').css('right', '-200px');
    $('#toasty-darth').css('bottom', '-10px');
    $('body').append('<audio id="toasty-audio"><source src="/static/libraries/misc/nooo.mp3" type="audio/mpeg"></audio>');
    $('.disabled').click(function (ev) {
        if (!$(ev.target).hasClass('disabled')) {
            return;
        }
        ev.preventDefault();
        console.log(ev);
        var audio = document.getElementById('toasty-audio');
        audio.play();
        $("#toasty-darth").addClass("show-darth");
        setTimeout(function () {
            $("#toasty-darth").removeClass("show-darth");
        }, 5000);
    });
});