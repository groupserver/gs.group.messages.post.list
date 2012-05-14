# coding=utf-8
from zope.cachedescriptors.property import Lazy
from zope.component import createObject
from Products.GSSearch.queries import MessageQuery

class PostsSearch(object):
    def __init__(self, group, limit, offset):
        self.context = self.group = group
        self.limit = limit
        self.offset = offset

