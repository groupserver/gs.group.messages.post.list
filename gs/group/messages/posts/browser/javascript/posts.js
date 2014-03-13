"use strict";
// GroupServer JavaScript module for providing the content of the Posts tab
//
// Copyright © 2013, 2014 OnlineGroups.net and Contributors.
// All Rights Reserved.
//
// This software is subject to the provisions of the Zope Public License,
// Version 2.1 (ZPL). http://groupserver.org/downloads/license/
//
jQuery.noConflict();

function gs_group_messages_posts_init_search() {
    var postsSearch=null;

    function posts_show (event, ui) {
        if (!postsSearch.results_shown()) {
            postsSearch.load();
        }
    }

    function get_url() {
        var b=null, retval=null;
        b = jQuery('base').attr('href');
        if (b[b.length -1] != '/') {
            b = b + '/';
        }
        retval = b + 'gs-group-messages-posts-ajax.html';
        return retval;
    }
    
    postsSearch = GSSearch('#gs-group-messages-posts-search', 
                           get_url(), 0, 12, {}, null);
    jQuery('#gs-group-messages-base-tab-1 a').click(posts_show);
}


jQuery(window).load(function () {
    gsJsLoader.with_module('/++resource++gs-search-base-js-min-20140313.js',
                           gs_group_messages_posts_init_search);
});
