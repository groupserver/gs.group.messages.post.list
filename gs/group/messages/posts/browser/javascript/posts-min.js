"use strict";jQuery.noConflict();function gs_group_messages_posts_init_search(){var c=null;
function b(d,e){if(!c.results_shown()){c.load()}}function a(){var d=null,e=null;d=jQuery("base").attr("href");
if(d[d.length-1]!="/"){d=d+"/"}e=d+"gs-group-messages-posts-ajax.html";return e}c=GSSearch("#gs-group-messages-posts-search",a(),0,12,{},null);
jQuery("#gs-group-messages-base-tab-1 a").click(b)}jQuery(window).load(function(){gsJsLoader.with_module("/++resource++gs-search-base-js-min-20140313.js",gs_group_messages_posts_init_search)
});