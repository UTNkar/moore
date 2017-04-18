$(".top-action").click(function(ev) {
    ev.preventDefault();
   $("html, body").animate({scrollTop: 0}, 1000);
});