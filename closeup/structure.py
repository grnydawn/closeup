# -*- coding: UTF-8 -*-
"""Implement functions handling structures.
"""
from __future__ import absolute_import, division, print_function, unicode_literals
import re, os, json
from . import util

#######################################################################
#   Internal Functions
#######################################################################

#def split_name(name):
#    parsed = []
#    for item in name.split('/'):
#        poslb = item.find('[')
#        posrb = item.find(']')
#        if poslb<=0 or posrb<=0 or posrb<=poslb or \
#            (posrb+1)!=len(item) or not item[poslb+1:posrb].isdigit():
#            parsed.append((item, None))
#        else:
#            parsed.append((item[:poslb], int(item[poslb+1:posrb])))
#    return parsed
#
#def parse_name(name):
#    """Split and parse name into namepath."""
#    reg_name_list = []
#    obj_name_list = split_name(name)
#    cur_dict = read_register()
#    for item_name, index in list(obj_name_list):
#        if item_name not in cur_dict:
#            return reg_name_list, obj_name_list
#        if index is None:
#            cur_dict = cur_dict[item_name]
#        else:
#            cur_dict = cur_dict[item_name][index]
#        reg_name_list.append(obj_name_list.pop(0))
#    return reg_name_list, obj_name_list
#
#def set_dictnode(top_node, name, value, create=True):
#
#    splited = split_name(name)
#    cur_node = top_node
#    for item, index in splited[:-1]:
#        if item in cur_node:
#            if isinstance(index, int):
#                cur_node = cur_node[item][index]
#            else:
#                cur_node = cur_node[item]
#        elif create:
#            if isinstance(index, int):
#                cur_node[item] = [dict()]*(index+1)
#                cur_node = cur_node[item][index]
#            else:
#                cur_node[item] = dict()
#                cur_node = cur_node[item]
#        else:
#            raise ValueError('"{}" does not exists in "{}".'.format(item, name))
#    if splited[-1][0] in cur_node:
#        raise ValueError('"{}" already exists in "{}".'.format(splited[0], name))
#    if isinstance(splited[-1][1], int):
#        cur_node[splited[-1][0]] = [None]*(splited[-1][1]+1)
#        cur_node[splited[-1][0]][splited[-1][1]] = value
#    else:
#        cur_node[splited[-1][0]] = value
#
#def is_leaf(e):
#    return isinstance(e, list) and len(e)==2 and isinstance(e[0],str) and \
#        isinstance(e[1],dict) and 'reg_type' in e[1]
#
#def are_leaves(e):
#    return isinstance(e, list) and all(is_leaf(_e) for _e in e)
#
#def get_leaves(e):
#    for k, v in e.items():
#        if are_leaves(v):
#            for _v in v:
#                yield _v
#        else:
#            get_leaves(v)

#######################################################################
#  Classes
#######################################################################

class Name(object):

    delimiter = '/'

    def __init__(self, name):
        self.name = name
        self.pairs = self._split_name(name)
        self.idx = 0

    def __iter__(self):
        return self

    def __next__(self):
        self.idx += 1
        try:
            return self.pairs[self.idx-1]
        except IndexError:
            self.idx = 0
            raise StopIteration

    next = __next__

    def _split_name(self, name):
        pairs = []
        raw_pairs = name.strip().strip('/').split(self.delimiter)
        for raw_pair in raw_pairs:
            match = re.match(r'^(?P<ident>[^/\x00]+)\[(?P<index>\d+)\]$', raw_pair)
            if match:
                pairs.append((match.group('ident'), int(match.group('index'))))
            else:
                match = re.match(r'^(?P<ident>[^/\x00]+)$', raw_pair)
                if match:
                    pairs.append((match.group('ident'), None))
                else:
                    raise Exception('Can not parse {}'.format(raw_pair))
        return pairs

    def __str__(self):
        pairs = [self.name]
        for ident, index in self:
            pairs.append((ident, str(index)))
        return str(pairs)

class Link(object):
    def __init__(self, item, attr):
        self.item = item
        self.attr = attr

# disallow update a node, rather allow delete and add
class Register(object):

    def __init__(self, path):
        self.path = path
        if os.path.exists(path):
            with open(path, 'r') as f:
                self.json = json.load(f)
        else:
            self.json = {}

    def _get_or_create(self, nameobj, create=True):
        last_parent = None
        identifier = None
        cur_node = self.json
        for ident, index in nameobj:
            if ident in cur_node:
                if isinstance(index, int):
                    last_parent = cur_node[ident]
                    identifier = index
                    if isinstance(cur_node[ident], list):
                        if index>=len(cur_node[ident]):
                            difflen = len(cur_node[ident]) - index + 1
                            cur_node[ident] += [{} for _ in range(difflen)]
                        cur_node = cur_node[ident][index]
                    else:
                        raise Exception('{} is alread exists but '+
                            'not a list.'.format(str(ident)))
                else:
                    last_parent = cur_node
                    identifier = ident
                    cur_node = cur_node[ident]
            elif create:
                if isinstance(index, int):
                    cur_node[ident] = [{} for _ in range(index+1)]
                    last_parent = cur_node[ident]
                    identifier = index
                    cur_node = cur_node[ident][index]
                else:
                    cur_node[ident] = {}
                    last_parent = cur_node
                    identifier = ident
                    cur_node = cur_node[ident]
            else:
                raise Exception('({},{}) is not in {}.'.format(
                    str(ident), str(index), str(nameobj)))
        return last_parent, identifier

    def _get(self, nameobj):
        return self._get_or_create(nameobj, create=False)

    def dump(self):
        with open(self.path, 'w') as f:
            json.dump(self.json, f)

    def add(self, name, items, attrs):
        nameobj = Name(name)
        last_parent, ident = self._get_or_create(nameobj)
        array = [ ('\x00', item, attrs) for item in items ]
        last_parent[ident] = array

    def remove(self, name):
        nameobj = Name(name)
        last_parent, identifier = self._get(nameobj)
        del last_parent[identifier]

    def get(self, name):
        nameobj = Name(name)
        last_parent, identifier = self._get(nameobj)
        return last_parent[identifier]

#######################################################################
#  Public Functions
#######################################################################

def load_register():
    return Register(util.regpath)
