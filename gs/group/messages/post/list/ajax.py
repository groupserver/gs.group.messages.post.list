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
from AccessControl import getSecurityManager
from gs.group.base import GroupPage
from .postssearch import PostsSearch


class PostsAjax(GroupPage):
    @Lazy
    def viewTopics(self):
        # TODO: Figure out I could do this better.
        msgs = self.context.messages
        user = getSecurityManager().getUser()
        retval = bool(user.has_permission('View', msgs))
        return retval

    @Lazy
    def offset(self):
        retval = int(self.request.get('i', 0))
        assert retval >= 0
        return retval

    @Lazy
    def limit(self):
        retval = int(self.request.get('l', 6)) % 48
        assert retval >= 0
        return retval

    @Lazy
    def searchTokens(self):
        s = self.request.get('s', '')
        return createObject('groupserver.SearchTextTokens', s)

    def posts(self):
        '''Generator, which returns the posts'''
        ps = PostsSearch(self.context, self.searchTokens, self.limit,
                         self.offset)
        return ps.posts()
