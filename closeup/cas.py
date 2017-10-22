# -*- coding: UTF-8 -*-
"""Implement Content Addressable Stroage."""

from __future__ import absolute_import, division, print_function, unicode_literals
import hashlib, zlib
from . import system, util

def objects_path(repo):
    return system.pathjoin(repo, '.closeup', 'objects')

def register_path(repo):
    return system.pathjoin(repo, '.closeup', 'register')

def image_path(repo):
    return system.pathjoin(repo, '.closeup', 'image')

def hash_object(data, obj_type, write=True):
    """Compute hash of object data of given type and write to object store if
    "write" is True. Return SHA-1 object hash as hex string.
    """
    header = util.to_bytes('{} {}'.format(obj_type, len(data)))
    full_data = header + b'\x00' + data
    sha1 = hashlib.sha1(full_data).hexdigest()
    if write:
        path = system.pathjoin('.closeup', 'objects', sha1[:2], sha1[2:])
        if not system.pathexists(path):
            try:
                system.makedirs(system.dirname(path))
            except:
                pass
            system.write_bytefile(path, zlib.compress(full_data))
    return sha1

