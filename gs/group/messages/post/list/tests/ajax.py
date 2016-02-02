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
from mock import MagicMock, patch
from unittest import TestCase
from gs.group.messages.post.list.ajax import (PostsAjax, )


class TestPostsAjax(TestCase):
    'Test the post-search AJAX'

    def test_limit(self):
        request = {'l': '9'}
        pa = PostsAjax(MagicMock(), request)
        r = pa.limit

        self.assertEqual(9, r)

    def test_limit_missing(self):
        request = {}
        pa = PostsAjax(MagicMock(), request)
        r = pa.limit

        self.assertEqual(6, r)

    def test_limit_max(self):
        request = {'l': '1024'}
        pa = PostsAjax(MagicMock(), request)
        r = pa.limit

        self.assertGreater(1024, r)

    def test_offset(self):
        request = {'i': '1024'}
        pa = PostsAjax(MagicMock(), request)
        r = pa.offset

        self.assertEqual(1024, r)

    def test_offset_missing(self):
        request = {}
        pa = PostsAjax(MagicMock(), request)
        r = pa.offset

        self.assertEqual(0, r)

    @patch('gs.group.messages.post.list.ajax.createObject')
    def test_tokens(self, m_cO):
        request = {'s': 'Ethel the Frog'}
        pa = PostsAjax(MagicMock(), request)
        r = pa.searchTokens

        self.assertTrue(r)
        m_cO.assert_called_once_with('groupserver.SearchTextTokens', 'Ethel the Frog')

    @patch('gs.group.messages.post.list.ajax.createObject')
    def test_tokens_missing(self, m_cO):
        request = {}
        pa = PostsAjax(MagicMock(), request)
        r = pa.searchTokens

        self.assertTrue(r)
        m_cO.assert_called_once_with('groupserver.SearchTextTokens', '')
