# -*- coding: utf-8 -*-
from __future__ import absolute_import
from zope.i18nmessageid import MessageFactory
GSMessageFactory = MessageFactory('gs.group.messages.posts')
from .queries import PostSearchQuery  # lint:ok
