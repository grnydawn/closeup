# -*- coding: UTF-8 -*-
"""Implement json file handling functions.
"""

import os, json
from . import util, exception, filesys, namepath

class JSONFile(object):
    def __init__(self, path, json_types):
        self.path = path
        if os.path.exists(path):
            with open(path, 'r') as f:
                self.json = json.load(f)
        else:
            self.json = { t: {} for t in json_types }

    def add(self, reg_type, name_path, value, create_if_notexist=False):
        def _add(pardict, curkey, curpath):
            if curpath:
                if curkey in pardict:
                    if isinstance(curpath[0], int):
                        if not isinstance(pardict[curkey], list):
                            raise exception.NamePartTypeMismatchError(
                                list, type(pardict[curkey]))
                        if curpath[0]>=len(pardict[curkey]):
                            pardict[curkey] += [{} for _ in
                                range(curpath[0]+1-len(pardict[curkey]))]
                    elif isinstance(pardict[curkey], list):
                        raise exception.NamePartTypeMismatchError(
                            type(pardict[curkey]), list)
                elif create_if_notexist:
                    if isinstance(curpath[0], int):
                        pardict[curkey] = [{} for _ in range(curpath[0]+1)]
                    else:
                        pardict[curkey] = {}
                else:
                    raise exception.NamePartNotExistError(curpath[0], name_path)
                _add(pardict[curkey], curpath[0], curpath[1:])
            else:
                pardict[curkey] = value
        _add(self.json[reg_type], name_path[0], list(name_path[1:]))

    def dump(self):
        with open(self.path, 'w') as f:
            json.dump(self.json, f)

    def traverse(self, node, check, func):
        if check(node):
            func(node)
        else:
            if isinstance(node, dict):
                for _, v in node.items():
                    self.traverse(v, check, func)
            elif isinstance(node, list):
                for i in node:
                    self.traverse(i, check, func)

    def __str__(self):
        return json.dumps(self.json, sort_keys=True)

class Register(JSONFile):
    def __init__(self):
        super(Register, self).__init__(util.register_path, [util.register_type])

    def hash_object(self):
        self.traverse( self.json, self.ishashable, self.dohashing)

    def ishashable(self, item):
        if isinstance(item, list) and len(item)==4 and item[0]=='\x00' \
            and isinstance(item[2], dict) and 'reg_type' in item[2]:
            return True
        return False

    def dohashing(self, item):
        _, content, attrs, hashed = item
        item[3] = filesys.hashingmap[attrs['reg_type']](content)

    def add(self, reg_type, name_obj, value):
        super(Register, self).add(reg_type, name_obj.path, value,
            create_if_notexist=True)

class Album(JSONFile):
    def __init__(self):
        super(Album, self).__init__(util.album_path,
            [util.image_type, util.group_type])

    def add(self, album_type, name_obj, value):
        super(Album, self).add(album_type, name_obj.path, value,
            create_if_notexist=True)

def load_register():
    return Register()

def load_album():
    return Album()

def generate_image_name_object(parent):
    return namepath.parse('image01')
