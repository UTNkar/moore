$(document).ready(function() {
    function deleteItem(btn, ev) {
       ev.preventDefault();

       $(btn).parents('.item').hide();

       var delbox = $(btn).parents('.delete-button').find('input[type=checkbox]');

       delbox.prop('checked', true);
    }

    $('#add').click(function(ev) {
        ev.preventDefault();
        var count = $('#formset-container').children().length;
        var tmplMarkup = $('#formset-template').html();
        var compiledTmpl = tmplMarkup.replace(/__prefix__/g, count);
        $('div#formset-container').append(compiledTmpl);

        $('.delete').click(function(ev) {
            return deleteItem(this, ev);
        });

        // update form count
        // TODO: make non-specific to references
        $('#id_references-TOTAL_FORMS').attr('value', count+1);
    });

    $('.delete').click(function(ev) {
        return deleteItem(this, ev);
    });
});