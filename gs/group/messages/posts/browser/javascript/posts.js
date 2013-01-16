jQuery.noConflict();
jQuery(document).ready( function () {
    var postsSearch = null;
    var show_posts = null;
    postsSearch = GSSearch('#gs-group-messages-posts-search', 
                           'gs-group-messages-posts-ajax.html', 
                           0, 12, {}, null);
    show_posts = function(event, ui) {
        // Tab counting starts at 0. Posts are the second tab.
        if ((ui.newPanel.attr('id') ===  'gs-group-messages-base-tabs-1') && 
            (!postsSearch.results_shown())) {
            postsSearch.load();
        }
    };
    jQuery('#gs-group-messages-base-tabs').on('tabsactivate', show_posts);
});
