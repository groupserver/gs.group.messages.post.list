Introduction
============

When a member posts a message to a group it is *normally* displayed in
a topic [#topic]_. However, people do not always want to see the 
messages organised in topics, they want a temporal view of the posts.
This module provides two such views:

#.  `The Posts Summary Tab`_ and
#.  `The Posts Page`_.

The Posts Summary Tab
=====================

The *Posts Summary* tab appears on the *Group* page [#group]_, as part 
of the *Tasks* grouping of tabs. This tab is designed to support one 
task:

  Determine **who** posted **where.**

To this end, the tab displays a four-column table: 

* Author (who)
* Topic (where)
* Files (what)
* Date (when)

The last two columns are nice-to-have, but are not needed. The *Posts
Summary* is less important than the topics, so it is displayed after
the *Topics* tab.

Supporting the *Posts* tab is a metadata-link to the *ATOM* feed for the
latest posts [#ATOM]_, and a link to `the Posts page`_.

The Posts Page
==============

The *Posts* page display all the posts made to a GroupServer group
[#posts]_. The display is much like that in a topic, except the
topic-title appears at the start of the post metadata.

..  Resources

..  [#topic]  Topics are displayed by the ``gs.group.messages.topic`` 
    product.
..  [#group]  The group page is provided by the ``gs.group.home`` 
    product.
..  [#ATOM]   The ATOM feed is rendered by the ``Products.GSSearch``
    product.
..  [#posts]  Each posts is displayed by the ``gs.group.messages.post`` 
    product.

