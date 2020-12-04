$(document).ready(function(){
    $(".button-collapse").sideNav();
    $(".dropdown-button").dropdown({
        hover: true
    });

    /**
     * Moves the dropdown menu in the navigation bar on hover
     * if the user has scrolled in the navigation bar. This behaviour
     * does not exist in materialize so it had to be added manually.
     */
    $("nav .main-menu > .dropdown-button").hover(function() {
        const elementToActivateId = this.dataset.activates;
        const elementToActivate = $(`#${elementToActivateId}`)

        const dropDownLeft = parseInt(elementToActivate.css("left"));
        const buttonLeft = Math.floor($(this).offset().left);
        const currentScrollLeft = $("nav .main-menu").scrollLeft();

        if (buttonLeft == dropDownLeft - currentScrollLeft){
            elementToActivate.css("left", dropDownLeft - currentScrollLeft)
        }
    }, function(){
        /*
         * This empty function is needed so that the above function
         * doesn't get runned on hover in and hover out
         */
    });
});
