# -*- coding: UTF-8 -*-
"""Implement sub commands."""

from __future__ import absolute_import, division, print_function, unicode_literals
from . import system, error

def traverse(node, check=None):
    if check:
        if check(node):
            yield node
    else:
        yield node
    if isinstance(node, dict):
        for _, v in node.items():
            for n in traverse(v, check=check):
                yield n
    elif isinstance(node, list):
        for i in node:
            for n in traverse(i, check=check):
                yield n

def parse(name):
    namepath = []
    if not name:
        return name
    namelist = name.split(system.pathsep)
    for item in namelist:
        if item:
            pos = item.find('[')
            if pos>0 and item[-1]==']' and item[pos+1:-1].isdigit():
                namepath.append(item[:pos])
                namepath.append(int(item[pos+1:-1]))
            else:
                namepath.append(item)
        else:
            raise error.WrongNamePath(name, item)
    return namepath

def get(top, name):
    namepath = parse(name)
    for idx, node in enumerate(namepath):
        try:
            top = top[node]
        except TypeError as err:
            raise error.PathTypeMismatch(top, namepath[:idx],
                namepath[idx:])
        except KeyError as err:
            raise error.NamePathNotFound(namepath, node)
    return top

def set(top, name, value, overwrite=False):
    namepath = parse(name)
    if len(namepath)==0:
        raise error.WrongNamePath(name, '')
    elif len(namepath)==1:
        if isinstance(namepath[0], int):
            if not isinstance(top, list):
                raise error.PathTypeMismatch(list, type(top))
            if len(top)<=namepath[0]:
                top += [list() for _ in range(namepath[0]-len(top)+1)]
        else:
            if not isinstance(top, dict):
                raise error.PathTypeMismatch(dict, type(top))
        if namepath[0] in top and not overwrite:
            raise error.NamePathExists(name, namepath[0])
        top[namepath[0]] = value
    else:
        for parent, child in zip(namepath[:-1], namepath[1:]):
            if isinstance(child, int):
                ctype = list
            else:
                ctype = dict
            if isinstance(parent, int):
                if not isinstance(top, list):
                    raise error.PathTypeMismatch(list, type(top))
                if len(top)<=parent:
                    top += [ctype() for _ in range(parent-len(top)+1)]
            else:
                if not isinstance(top, dict):
                    raise error.PathTypeMismatch(dict, type(top))
                if parent not in top:
                    top[parent] = ctype()
            top = top[parent]

        if child in top and not overwrite:
            raise error.NamePathExists(name, child)
        top[child] = value
