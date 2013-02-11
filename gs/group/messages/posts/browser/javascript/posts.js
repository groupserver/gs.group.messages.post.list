init_post_search = function () {
    var postsSearch = null;
    var show_posts = null;
    var b = null;
    var url = null;

    jQuery.noConflict();

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


window.addEventListener('load', function () {
    gsJsLoader.with_modules(['/++resource++jquery-1.8.3.js',
                             '/++resource++bootstrap-2.2.2/js/bootstrap.js',
                             '/++resource++gs-search-base-js-20121217.js'],
                            init_post_search);
}, false);
