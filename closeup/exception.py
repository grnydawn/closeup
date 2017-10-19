# -*- coding: UTF-8 -*-
"""Implement Closeup Exceptions.
"""


class CloseupException(Exception):
    pass

class NamePartNotExistError(CloseupException):
    def __init__(self, part, name_obj):
        m = '"{}" of "{}" is not found.'.format(part, name_obj)
        self.part = part
        self.name_obj = name_obj
        super(CloseupException, self).__init__(m)

class NamePartTypeMismatchError(CloseupException):
    def __init__(self, expected, actual):
        m = 'type "{}" is expected but type "{}" is given.'.format(expected.__name__, actual.__name__)
        self.expected = expected
        self.actual = actual
        super(CloseupException, self).__init__(m)
