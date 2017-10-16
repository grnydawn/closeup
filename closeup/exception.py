# -*- coding: UTF-8 -*-
"""Implement closeup exceptions.
"""
from __future__ import absolute_import, division, print_function, unicode_literals

class CloseupException(Exception):
    pass

class CloseupNameError(CloseupException):
    pass

class NameParserError(CloseupNameError):
    pass

class NameAlreadyExistError(CloseupNameError):
    pass

class NameNotFoundError(CloseupNameError):
    pass

class NameNotAListError(CloseupNameError):
    pass

class NameNotALinkError(CloseupNameError):
    pass
