# -*- coding: utf-8 *-*


def to_unicode(s):
    u'''Ensure that a string (s) is in Unicode.'''
    # TODO: Make "to_unicode" a generic utility
    retval = s
    if not isinstance(s, unicode):
        retval = unicode(s, 'utf-8')
    return retval
