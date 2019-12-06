$(document).ready(function() {
    $('#application-form').dirrty().on('dirty', function(){
        $('#submit').removeClass('disabled');
    }).on('clean', function(){
        $('#submit').addClass('disabled');
    });

    $('.modal').modal();
});