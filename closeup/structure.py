# -*- coding: UTF-8 -*-
"""Implement functions handling structures.
"""
from __future__ import absolute_import, division, print_function, unicode_literals
import re, os, json, logging, hashlib
from . import util, exception

#######################################################################
#   Internal Functions
#######################################################################

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

    def __getitem__(self, sliced):
        return self.pairs[sliced]

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
                    raise exception.NameParserError('Can not parse {}'.format(raw_pair))
        return pairs

    def __str__(self):
        pairs = []
        for ident, index in self:
            if isinstance(index, int):
                pairs.append('{}[{:d}]'.format(ident,index))
            else:
                pairs.append(ident)
        return '/'.join(pairs)

    @classmethod
    def pack(cls, nameobj):
        obj = cls('dummy')
        obj.pairs = nameobj
        return str(obj)


# disallow update a node, rather allow delete and add
class NameBook(object):

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
                        raise exception.NameNotAListError('"{}" is alread exists but '+
                            'not a list.'.format(str(ident)))
                else:
                    if isinstance(cur_node[ident], list) and \
                        not is_link(cur_node[ident]):
                        raise exception.NameNotALinkError('"{}" is a list but '.format(str(ident))+
                            'index is not specified at "{}".'.format(Name.pack(nameobj)))
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
                raise exception.NameNotFoundError('({},{}) is not in {}.'.format(
                    str(ident), str(index), str(nameobj)))
        return last_parent, identifier

    def _get(self, nameobj):
        return self._get_or_create(nameobj, create=False)

    def dump(self):
        with open(self.path, 'w') as f:
            json.dump(self.json, f)

    def add(self, name, items, attrs):
        raise NotImplemented('Subclass should implement "add" method.')

    def remove(self, name):
        nameobj = Name(name)
        last_parent, identifier = self._get(nameobj)
        del last_parent[identifier]

    def get(self, name):
        nameobj = Name(name)
        last_parent, identifier = self._get(nameobj)
        return last_parent[identifier]

    def get_hash(self):
        return hashlib.sha1(json.dumps(self.json, separators=(',',':')).encode()).hexdigest()

class Register(NameBook):

    def add(self, name, items, attrs):
        nameobj = Name(name)
        last_parent, ident = self._get_or_create(nameobj)
        array = [ ['\x00', item, attrs] for item in items ]
        last_parent[ident] = array

class Album(NameBook):

    def add(self, name, sha):
        nameobj = Name(name)
        last_parent, ident = self._get_or_create(nameobj)
        last_parent[ident] = sha

#######################################################################
#  Public Functions
#######################################################################

def load_register():
    return Register(util.regpath)

def register_split_name(name):
    """split name into register name and remained name."""
    logging.debug('calling register_split_name({})'.format(name))
    register = load_register()
    nameobj = Name(name)
    reg_name = list()
    rem_name = list()
    reg_parent, reg_key, reg_data = None, None, None
    for i, n in enumerate(nameobj):
        try:
            reg_parent, reg_key = register._get(nameobj[:i+1])
        except exception.CloseupNameError as err:
            break
        finally:
            if reg_parent and reg_key:
                reg_name = nameobj[:i+1]
                rem_name = nameobj[i+2:]
                reg_data = reg_parent[reg_key]
    return reg_name, reg_data, rem_name

def is_link(link):
    def _is_link(item):
        return isinstance(item, list) and len(item)==3 and \
            item[0]=='\x00' and isinstance(item[2], dict) and \
            'reg_type' in item[2]
    return isinstance(link, list) and all( _is_link(item) for item in link)

def is_leaf(leaf):
    return not isinstance(leaf, list) and not isinstance(leaf, dict)

def get_leaves(dictnode, func, bag=[]):
    for k, v in dictnode.items():
        if func(v):
            bag += v
        elif isinstance(v, list):
            for _v in v:
                get_leaves(_v, func)
        elif isinstance(v, dict):
            get_leaves(v, func)
    return bag

def get_links(dictnode, bag=[]):
    return get_leaves(dictnode, is_link)

def pack_name(nameobj):
    return Name.pack(nameobj)

def load_album():
    return Album(util.albumpath)

def image_split_name(name):
    """split name into image name and remained name."""
    logging.getLogger('closeup').debug('calling image_split_name({})'.format(name))
    album = load_album()
    nameobj = Name(name)
    img_name = list()
    rem_name = list()
    img_parent, img_key, img_data = None, None, None
    for i, n in enumerate(nameobj):
        try:
            img_parent, img_key = album._get(nameobj[:i+1])
        except exception.CloseupNameError as err:
            logging.getLogger('closeup').debug('{}'.format(err))
            break
        finally:
            if img_parent and img_key:
                img_name = nameobj[:i+1]
                rem_name = nameobj[i+2:]
                img_data = img_parent[img_key]
    return img_name, img_data, rem_name

