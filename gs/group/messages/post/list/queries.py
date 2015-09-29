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
import sqlalchemy as sa
from gs.core import to_unicode_or_bust
from gs.database import getTable, getSession


class PostSearchQuery(object):

    def __init__(self):
        self.postTable = getTable('post')
        self.fileTable = getTable('file')

    def add_standard_where_clauses(self, statement, site_id, group_ids,
                                   hidden):
        statement.append_whereclause(self.postTable.c.site_id == site_id)
        if group_ids:
            inStatement = self.postTable.c.group_id.in_(group_ids)
            statement.append_whereclause(inStatement)
        else:
            # --=mpj17=-- No, I am not smoking (much) crack. If the
            #  "group_ids" are not specified, I want to return nothing in
            #  all cases. However, I cannot append "False" to the
            #  statement, so I append two items that are mutually
            #  exclusive.
            statement.append_whereclause(self.postTable.c.group_id == '')
            statement.append_whereclause(self.postTable.c.group_id != '')
        if not(hidden):
            # We normally want to exclude hidden posts and topics.
            statement.append_whereclause(self.postTable.c.hidden == None)  # lint:ok
        return statement

    def files_metadata(self, post_id):
        """ Retrieve the metadata of all files associated with this post.

            Returns:
                [{'file_id': ID, 'mime_type': String,
                 'file_name': String, 'file_size': Int}]
             or
                []"""
        ft = self.fileTable
        statement = ft.select()
        statement.append_whereclause(ft.c.post_id == post_id)

        session = getSession()
        r = session.execute(statement)
        retval = []
        if r.rowcount:
            retval = [{'file_id': row['file_id'],
                       'file_name': to_unicode_or_bust(row['file_name']),
                       'date': row['date'],
                       'mime_type': to_unicode_or_bust(row['mime_type']),
                       'file_size': row['file_size']} for row in r]
        return retval

    def add_search_where_clauses(self, statement, searchTokens):
        # TODO Look at <https://sqlalchemy-searchable.readthedocs.org/>
        if searchTokens.keywords:  # --=mpj17=-- Change to phrases
            # --=mpj17=-- Note that the following call to the "match()"
            # method is one of the reasons that GroupServer *requires*
            # PostgreSQL.
            q = '&'.join(searchTokens.keywords)
            m = self.postTable.c.fts_vectors.match(q)
            statement.append_whereclause(m)

    def search(self, searchTokens, site_id, group_ids, limit=12, offset=0):
        '''Search the posts for the tokens in "searchTokens".'''
        pt = self.postTable
        cols = [pt.c.post_id, pt.c.user_id, pt.c.group_id,
                pt.c.subject, pt.c.date, pt.c.body, pt.c.has_attachments]
        statement = sa.select(cols, limit=limit, offset=offset,
                              order_by=sa.desc(pt.c.date))

        self.add_standard_where_clauses(statement, site_id, group_ids,
                                        False)
        self.add_search_where_clauses(statement, searchTokens)

        session = getSession()
        r = session.execute(statement)
        retval = []
        for x in r:
            p = {
                'post_id': x['post_id'],
                'user_id': x['user_id'],
                'group_id': x['group_id'],
                'subject': x['subject'],
                'date': x['date'],
                'body': x['body'],
                'files_metadata':
                self.files_metadata(x['post_id'])
                if x['has_attachments'] else [],
            }
            retval.append(p)
        return retval
