jQuery.noConflict();

function init_post_search() {
    var postsSearch = null, show_posts = null, b = null, url = null;

    b = jQuery('base').attr('href');
    if (b[b.length -1] != '/') {
      b = b + '/';
    }
    url = b + 'gs-group-messages-posts-ajax.html';

    postsSearch = GSSearch('#gs-group-messages-posts-search', 
                           url, 0, 12, {}, null);
    show_posts = function(event, ui) {
        if (!postsSearch.results_shown()) {
            postsSearch.load();
        }
    };
    jQuery('a[href="#gs-group-messages-base-tabs-1"]').on('click', show_posts);
}


jQuery(window).load(function () {
    gsJsLoader.with_module('/++resource++gs-search-base-js-min-20121217.js',
                           init_post_search);
});
