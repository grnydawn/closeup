# -*- coding: UTF-8 -*-
"""Implement namepath handling functions.
"""

from __future__ import absolute_import, division, print_function, unicode_literals
from . import util

class NamePath(object):
    def __init__(self, name):
        self.name = name
        self.path = []
        self.idx = 0
        for part in self.name.split(util.name_delimiter):
            if not part:
                continue
            if part[-1]==']':
                pos = part.rfind('[')
                if pos>0 and part[pos+1:-1].isdigit():
                    self.path.append(part[:pos])
                    self.path.append(int(part[pos+1:-1]))
                else:
                    self.path.append(part)
            else:
                self.path.append(part)

    def __iter__(self):
        return self

    def __next__(self):
        self.idx += 1
        try:
            return self.path[self.idx-1]
        except IndexError:
            self.idx = 0
            raise StopIteration

    next = __next__

    def match(self, jsondata):
        print ('BBBBB')

def parse(name):
    return NamePath(name)

def pack(np):
    items = []
    for item in np.path:
        if isinstance(item, int):
            items[-1] += '[{:d}]'.format(item)
        else:
            items.append(item)
    return '/'.join(items)


