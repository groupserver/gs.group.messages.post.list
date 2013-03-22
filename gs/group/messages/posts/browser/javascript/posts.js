jQuery.noConflict();

function gs_group_messages_posts_init_search() {
    var postsSearch = null;

    function posts_show (event, ui) {
        if (!postsSearch.results_shown()) {
            postsSearch.load();
        }
    }
    function get_url() {
        var b = null;
        b = jQuery('base').attr('href');
        if (b[b.length -1] != '/') {
            b = b + '/';
        }
        return b + 'gs-group-messages-posts-ajax.html';
    }
    
    postsSearch = GSSearch('#gs-group-messages-posts-search', 
                           get_url(), 0, 12, {}, null);
    jQuery('#gs-group-messages-base-tab-1 a').click(posts_show);
}


jQuery(window).load(function () {
    gsJsLoader.with_module('/++resource++gs-search-base-js-min-20121217.js',
                           gs_group_messages_posts_init_search);
});
