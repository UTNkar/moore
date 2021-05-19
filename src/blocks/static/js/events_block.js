class EventsBlockDefinition extends window.wagtailStreamField.blocks.StructBlockDefinition {
    render(placeholder, prefix, initialState, initialError) {
        const block = super.render(placeholder, prefix, initialState, initialError);

        const map = {};
        map['#' + prefix + '-show_facebook'] = '#' + prefix + '-facebook_page_name';
        map['#' + prefix + '-show_youtube'] = '#' + prefix + '-youtube_channel_id';
        map['#' + prefix + '-show_google_calendar'] = '#' + prefix + '-google_calendar_id';
        map['#' + prefix + '-show_instagram'] = '#' + prefix + '-instagram_account_name';

        function showHideField($checkbox) {
            var key = '#' + $checkbox.attr('id');
            var field = $(map[key]).parents('.field').parents('.field').first();
            // update the visibility of field according to the state of
            // the checkbox
            if ($checkbox.is(':checked')) {
                field.show();
            } else {
                field.hide();
            }
        }

        const $checkboxes = $(Object.keys(map).join(','));
        $checkboxes.each(function () {
            showHideField($(this));
        });
        $checkboxes.change(function() {
            showHideField($(this));
        });

        return block;
    }
}
window.telepath.register('moore.blocks.EventsBlock', EventsBlockDefinition);
