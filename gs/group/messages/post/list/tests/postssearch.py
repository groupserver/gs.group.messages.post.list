# -*- coding: utf-8 -*-
############################################################################
#
# Copyright © 2016 OnlineGroups.net and Contributors.
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
from __future__ import absolute_import, unicode_literals, print_function
from mock import MagicMock, patch, PropertyMock
from unittest import TestCase
from gs.group.messages.post.list.postssearch import (PostsSearch, )


class TestPostsSearch(TestCase):
    'Test the post-search generator'

    @property
    def authorInfo(self):
        ai = MagicMock()
        ai.id = 'example'
        ai.anonymous = False
        ai.url = '/p/example'
        ai.name = 'Example User'
        return ai

    def test_marshall_author_info(self):
        ps = PostsSearch(group=MagicMock(), searchTokens=MagicMock, limit=12, offset=0)
        r = ps.marshall_author_info(self.authorInfo)

        self.assertIn('id', r)
        self.assertIn('exists', r)
        self.assertTrue(r['exists'])
        self.assertIn('url', r)
        self.assertIn('name', r)

    @patch.object(PostsSearch, 'authorCache', new_callable=PropertyMock)
    def test_author_for_post_cached(self, m_aC):
        'Test that we get the cached author'
        ps = PostsSearch(group=MagicMock(), searchTokens=MagicMock, limit=12, offset=0)
        fakeReturn = {'id': 'example', 'exists': True, 'url': '/p/example', 'name': 'Example User'}
        ps.authorCache.get.return_value = fakeReturn
        post = {'user_id': 'example', }
        r = ps.author_for_post(post)

        ps.authorCache.get.assert_called_once_with('example')
        self.assertEqual(fakeReturn, r)

    @patch.object(PostsSearch, 'authorCache', new_callable=PropertyMock)
    @patch.object(PostsSearch, 'marshall_author_info')
    @patch('gs.group.messages.post.list.postssearch.createObject')
    def test_author_for_post_cache_miss(self, m_cO, m_mai, m_aC):
        'Test when we fail to retrieve a cached author'
        ps = PostsSearch(group=MagicMock(), searchTokens=MagicMock, limit=12, offset=0)
        cacheReturn = {}
        ps.authorCache.get.return_value = cacheReturn
        fakeReturn = {'id': 'example', 'exists': True, 'url': '/p/example', 'name': 'Example User'}
        m_mai.return_value = fakeReturn
        post = {'user_id': 'example', }
        r = ps.author_for_post(post)

        ps.authorCache.get.assert_called_once_with('example')
        self.assertEqual(fakeReturn, r)
