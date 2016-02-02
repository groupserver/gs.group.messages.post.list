# -*- coding: utf-8 -*-
############################################################################
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
############################################################################
from __future__ import absolute_import, unicode_literals
from zope.cachedescriptors.property import Lazy
from zope.component import createObject
from gs.core import to_ascii
from Products.XWFCore.cache import LRUCache
from .queries import PostSearchQuery


class PostsSearch(object):

    authorCache = LRUCache("Author")

    def __init__(self, group, searchTokens, limit, offset):
        self.context = self.group = group
        self.searchTokens = searchTokens
        self.limit = limit
        self.offset = offset

    @Lazy
    def groupInfo(self):
        retval = createObject('groupserver.GroupInfo', self.context)
        return retval

    @Lazy
    def siteInfo(self):
        retval = createObject('groupserver.SiteInfo', self.context)
        return retval

    @Lazy
    def loggedInUser(self):
        retval = createObject('groupserver.LoggedInUser', self.context)
        return retval

    @Lazy
    def postSearchQuery(self):
        retval = PostSearchQuery()
        return retval

    def posts(self):
        posts = self.rawPostInfo
        for post in posts:
            post['files'] = post['files_metadata']
            post['author'] = self.author_for_post(post)
            yield post

    @Lazy
    def rawPostInfo(self):
        retval = self.postSearchQuery.search(
            self.searchTokens, self.siteInfo.id, [self.groupInfo.id],
            self.limit, self.offset)
        assert type(retval) == list
        return retval

    def author_for_post(self, post):
        uid = post['user_id']
        retval = self.authorCache.get(uid)
        if not retval:
            authorInfo = createObject('groupserver.UserFromId', self.context, uid)
            retval = self.marshall_author_info(authorInfo)
            self.authorCache.add(uid, retval)
        assert type(retval) == dict
        return retval

    @staticmethod
    def marshall_author_info(authorInfo):
        retval = {
            'id': authorInfo.id,
            'exists': not authorInfo.anonymous,
            'url': to_ascii(authorInfo.url),
            'name': authorInfo.name,
        }
        return retval
