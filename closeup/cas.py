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

def hash_object(repo, data, obj_type, write=True):
    header = util.to_bytes('{} {}'.format(obj_type, len(data)))
    full_data = header + b'\x00' + data
    sha1 = hashlib.sha1(full_data).hexdigest()
    if write:
        path = system.pathjoin(repo, '.closeup', 'objects', sha1[:2], sha1[2:])
        if not system.pathexists(path):
            try:
                system.makedirs(system.dirname(path))
            except:
                pass
            system.write_bytefile(path, zlib.compress(full_data))
    return sha1

def find_object(repo, sha1_prefix):
    if len(sha1_prefix) < 2:
        raise ValueError('hash prefix must be 2 or more characters')
    obj_dir = system.pathjoin(repo, '.closeup', 'objects', sha1_prefix[:2])
    rest = sha1_prefix[2:]
    objects = [name for name in system.listdir(obj_dir) if name.startswith(rest)]
    if not objects:
        raise ValueError('object {!r} not found'.format(sha1_prefix))
    if len(objects) >= 2:
        raise ValueError('multiple objects ({}) with prefix {!r}'.format(
                len(objects), sha1_prefix))
    return system.pathjoin(obj_dir, objects[0])

def read_object(repo, sha1_prefix):
    path = find_object(repo, sha1_prefix)
    full_data = zlib.decompress(system.read_bytefile(path))
    nul_index = full_data.index(b'\x00')
    header = full_data[:nul_index]
    obj_type, size_str = util.to_unicodes(header).split()
    size = int(size_str)
    data = full_data[nul_index + 1:]
    assert size == len(data), 'expected size {}, got {} bytes'.format(
            size, len(data))
    return (obj_type, data)
