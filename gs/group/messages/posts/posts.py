# -*- coding: utf-8 -*-
##############################################################################
#
# Copyright © 2013, 2014 OnlineGroups.net and Contributors.
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#
##############################################################################
from __future__ import absolute_import, unicode_literals
from logging import getLogger
log = getLogger('gs.group.messages.posts.postsview.PostsView')
from zope.cachedescriptors.property import Lazy
from gs.core import to_ascii
from Products.XWFMailingListManager.queries import MessageQuery
from Products.GSGroup.utils import is_public
from gs.group.base import GroupPage


class PostsView(GroupPage):
    topNPosts = 64

    def __init__(self, context, request):
        super(PostsView, self).__init__(context, request)

        self.start = int(self.request.form.get('start', 0))
        self.end = int(self.request.form.get('end', 20))
        # Swap the start and end, if necessary
        if self.start > self.end:
            tmp = self.end
            self.end = self.start
            self.start = tmp
        nPosts = (self.end - self.start)
        if (nPosts > self.topNPosts):
            m = 'Request for %d posts (%d--%d) from %s (%s) on ' \
                '%s (%s) is too high; returning %d.' % \
                (nPosts, self.start, self.end, self.groupInfo.name,
                self.groupInfo.id, self.siteInfo.name,
                self.siteInfo.id, self.topNPosts)
            log.warn(m)
            self.end = self.start + self.topNPosts

    @Lazy
    def isPublic(self):
        return is_public(self.groupInfo.groupObj)

    @Lazy
    def messageQuery(self):
        retval = MessageQuery(self.context)
        return retval

    @Lazy
    def lists(self):
        messages = self.context.messages
        retval = messages.getProperty('xwf_mailing_list_ids')
        assert retval
        return retval

    @Lazy
    def numPosts(self):
        retval = self.messageQuery.post_count(self.siteInfo.get_id(),
                                              self.lists)
        assert retval >= 0, 'There are a negative number of posts!'
        return retval

    @Lazy
    def posts(self):
        limit = self.chunkLength
        retval = self.messageQuery.latest_posts(self.siteInfo.get_id(),
                                              self.lists, limit=limit,
                                              offset=self.start)

        return retval

    @Lazy
    def chunkLength(self):
        assert hasattr(self, 'start')
        assert hasattr(self, 'end')
        assert self.start <= self.end

        retval = self.end - self.start

        assert retval >= 0
        return retval

    def get_later_url(self):
        assert hasattr(self, 'start')

        newStart = self.start - self.chunkLength
        if newStart < 0:
            newStart = 0
        newEnd = newStart + self.chunkLength

        if newStart != self.start and newStart:
            url = 'posts.html?start=%d&end=%d' % (newStart, newEnd)
        elif newStart != self.start and not newStart:
            url = 'posts.html'
        else:
            url = ''
        retval = to_ascii(url)
        return retval

    def get_earlier_url(self):
        assert hasattr(self, 'end')

        newStart = self.end
        newEnd = newStart + self.chunkLength
        if newStart < self.numPosts:
            url = 'posts.html?start=%d&end=%d' % (newStart, newEnd)
        else:
            url = ''
        retval = to_ascii(url)
        return retval

    def get_last_url(self):
        newStart = self.numPosts - self.chunkLength
        newEnd = self.numPosts
        url = 'posts.html?start=%d&end=%d' % (newStart, newEnd)
        retval = to_ascii(url)
        return retval

    def get_most_recent_post_date(self):
        retval = ''
        if self.posts:
            mostRecentPost = self.posts[0]
            d = mostRecentPost['date']
            date = d - d.utcoffset()
            retval = date.strftime('%Y-%m-%dT%H:%M:%SZ')
        return retval

    @Lazy
    def web_feed_uri(self):
        uri = '/s/search.atom?g=%s&p=1&t=0&l=%d' % \
                (self.groupInfo.id, self.chunkLength)
        retval = to_ascii(uri)
        return retval
