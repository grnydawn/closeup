# -*- coding: UTF-8 -*-
"""Implement sub commands."""

from __future__ import absolute_import, division, print_function, unicode_literals
import logging
logger = logging.getLogger('closeup')

class CUPException(Exception):
    pass

class NoRepoRootFound(CUPException):
    def __init__(self, path, finalpath):
        self.path = path
        self.finalpath = finalpath

    def __str__(self):
        return 'fatal: Not a closeup repository (or any parent up to {})'.format(
            self.finalpath)

class WrongNamePath(CUPException):
    def __init__(self, namepath, nameitem):
        self.namepath = namepath
        self.nameitem = nameitem

    def __str__(self):
        return 'fatal: "{}" of "{}" caused namepath syntax error'.format(
            self.nameitem, self.namepath)

class NamePathExists(CUPException):
    def __init__(self, namepath, nameitem):
        self.namepath = namepath
        self.nameitem = nameitem

    def __str__(self):
        return 'fatal: "{}" of "{}" already exists.'.format(
            self.nameitem, self.namepath)

