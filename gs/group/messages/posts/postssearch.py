# coding=utf-8
from zope.cachedescriptors.property import Lazy
from zope.component import createObject
from Products.XWFCore.cache import LRUCache
from Products.GSSearch.queries import MessageQuery

class PostsSearch(object):

    authorCache = LRUCache("Author")

    def __init__(self, group, limit, offset):
        self.context = self.group = group
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
    def messageQuery(self):
        retval  = MessageQuery(self.context, self.da)
        return retval

    def posts(self):
        posts = self.rawPostInfo
        for post in posts:
            post['files']   =   post['files_metadata']
            post['author']  =   self.author_for_post(post)
            yield post

    @Lazy
    def rawPostInfo(self):
        searchTokens = createObject('groupserver.SearchTextTokens', '')
        retval = self.messageQuery.post_search_keyword(searchTokens,
              self.siteInfo.id, [self.groupInfo.id], [],
              limit=self.limit, offset=self.offset)
        assert type(retval) == list
        return retval
    
    def author_for_post(post):
        uid = post['user_id']
        authorInfo = authorCache.get(uid, None)
        if not authorInfo:
            authorInfo = createObject('groupserver.UserFromId', 
                                        self.context, uid)
            authorCache[uid] = authorInfo
        authorId = authorInfo.id
        retval = {
          'id':     authorInfo.id,
          'exists': not authorInfo.anonymous,
          'url':    authorInfo.url,
          'name':   authorInfo.name,
        }
        assert type(retval) == dict
        return retval

