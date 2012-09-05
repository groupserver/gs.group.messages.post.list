# -*- coding: utf-8 *-*
u'''The queries for searching all posts in a group.'''
import sqlalchemy as sa
from gs.database import getTable, getSession


class PostQuery(object):

    def __init__(self):
        self.postTable = getTable('post')

    def add_standard_where_clauses(self, statement, table,
                                   site_id, group_ids, hidden):
        statement.append_whereclause(table.c.site_id == site_id)
        if group_ids:
            inStatement = table.c.group_id.in_(group_ids)
            statement.append_whereclause(inStatement)
        else:
            # --=mpj17=-- No, I am not smoking (much) crack. If the
            #  "group_ids" are not specified, I want to return nothing in
            #  all cases. However, I cannot append "False" to the
            #  statement, so I append two items that are mutually
            #  exclusive.
            statement.append_whereclause(table.c.group_id == '')
            statement.append_whereclause(table.c.group_id != '')
        if not(hidden):
            # We normally want to exclude hidden posts and topics.
            statement.append_whereclause(table.c.hidden is None)  # works??
        return statement

    def __add_post_keyword_search_where_clauses(self, statement,
                                                  searchTokens):
        """Post searching is easier than topic searching, as there is no
          natural join between the topic and post tables."""
        pt = self.postTable

        if searchTokens.keywords:  # --=mpj17=-- Change to phrases
            q = '&'.join(searchTokens.keywords)
            # --=mpj17=-- Note that the following call to the "match()" method
            #    is one of the reasons that GroupServer *requires* PostgreSQL.
            statement.append_whereclause(pt.c.fts_vectors.match(q))
        return statement

    def post_search_keyword(self, searchTokens, site_id, group_ids=[],
                            limit=12, offset=0):
        pt = self.postTable
        cols = [pt.c.post_id.distinct(), pt.c.user_id, pt.c.group_id,
                  pt.c.subject, pt.c.date, pt.c.body, pt.c.has_attachments]
        statement = sa.select(cols, limit=limit, offset=offset,
                  order_by=sa.desc(pt.c.date))

        self.add_standard_where_clauses(statement, pt, site_id,
            group_ids, False)
        statement = self.__add_post_keyword_search_where_clauses(statement,
          searchTokens)

        session = getSession()
        r = session.execute(statement)
        retval = []
        for x in r:
            p = {
              'post_id':          x['post_id'],
              'user_id':          x['user_id'],
              'group_id':         x['group_id'],
              'subject':          x['subject'],
              'date':             x['date'],
              'body':             x['body'],
              'files_metadata':   x['has_attachments']
                                  and self.files_metadata(x['post_id'])
                                  or [],
              }
            retval.append(p)
        return retval
