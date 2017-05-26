$(document).ready(function() {
  $('.carousel.carousel-slider').carousel({
      fullWidth: true
  });
  $('.banners .search > input').click(function(e){});
  $('.carousel-next').click(function(){
    $(this).closest('.carousel').carousel('next');
  });
  $('.carousel-previous').click(function(){
    $(this).closest('.carousel').carousel('prev');
  })
});

