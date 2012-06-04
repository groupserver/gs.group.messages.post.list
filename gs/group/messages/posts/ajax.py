# coding=utf-8
from zope.cachedescriptors.property import Lazy
from zope.component import createObject
from AccessControl import getSecurityManager
from gs.group.base.page import GroupPage
from postssearch import PostsSearch

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
