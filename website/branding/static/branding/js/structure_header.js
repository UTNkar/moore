// Committee/Section header
$('#section-switch').click(function(ev) {
    ev.preventDefault();
    $('.committees').hide();
    $('.sections').show();
});
$('#committee-switch').click(function(ev) {
    ev.preventDefault();
    $('.sections').hide();
    $('.committees').show();
});