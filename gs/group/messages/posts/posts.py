# coding=utf-8
from zope.cachedescriptors.property import Lazy
from zope.component import createObject
import Products.Five, Products.GSContent, Globals
import zope.schema
import zope.pagetemplate.pagetemplatefile
import zope.interface, zope.component, zope.publisher.interfaces
from zope.component import createObject
import zope.viewlet.interfaces, zope.contentprovider.interfaces 
import DocumentTemplate, Products.XWFMailingListManager
import Products.GSContent, Products.XWFCore.XWFUtils
from Products.XWFMailingListManager.queries import MessageQuery
from Products.GSGroup.utils import is_public
from gs.group.base.page import GroupPage


import logging
log = logging.getLogger('gs.group.messages.posts.postsview.PostsView')

class PostsView(GroupPage):
    topNPosts = 64
    def __init__(self, context, request):
        GroupPage.__init__(self, context, request)

        self.start = int(self.request.form.get('start', 0))
        self.end = int(self.request.form.get('end', 20))
        # Swap the start and end, if necessary
        if self.start > self.end:
            tmp = self.end
            self.end = self.start
            self.start = tmp
        nPosts = (self.end - self.start)
        if (nPosts >  self.topNPosts):
            m = u'Request for %d posts (%d--%d) from %s (%s) on ' \
                u'%s (%s) is too high; returning %d.' % \
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
        da = self.context.zsqlalchemy 
        assert da
        retval = MessageQuery(self.context, da)
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
        assert retval
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
            retval = 'posts.html?start=%d&end=%d' % (newStart, newEnd)
        elif newStart != self.start and not newStart:
            retval = 'posts.html'
        else:
            retval = ''
        return retval

    def get_earlier_url(self):
        assert hasattr(self, 'end')

        newStart = self.end
        newEnd = newStart + self.chunkLength
        if newStart < self.numPosts:
            retval = 'posts.html?start=%d&end=%d' % (newStart, newEnd)
        else:
            retval = ''
        return retval

    def get_last_url(self):
        newStart = self.numPosts - self.chunkLength
        newEnd = self.numPosts
        return 'posts.html?start=%d&end=%d' % (newStart, newEnd)

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
        retval = '/s/search.atom?g=%s&p=1&t=0&l=%d' %\
          (self.groupInfo.id, self.chunkLength)
        assert type(retval) == str
        return retval

