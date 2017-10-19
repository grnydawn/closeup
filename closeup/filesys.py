# -*- coding: UTF-8 -*-
"""Implement cluseup file system."""

from __future__ import absolute_import, division, print_function, unicode_literals
import os, hashlib, zlib
from . import util

def hash_object(data, obj_type, write=True):
    """Compute hash of object data of given type and write to object store if
    "write" is True. Return SHA-1 object hash as hex string.
    """
    header = '{} {}'.format(obj_type, len(data)).encode()
    full_data = header + b'\x00' + data
    sha1 = hashlib.sha1(full_data).hexdigest()
    if write:
        path = os.path.join('.closeup', 'objects', sha1[:2], sha1[2:])
        if not os.path.exists(path):
            try:
                os.makedirs(os.path.dirname(path))
            except:
                pass
            util.write_bytefile(path, zlib.compress(full_data))
    return sha1

def get_local_master_hash():
    """Get current commit hash (SHA-1 string) of local master branch."""
    try:
        return read_file(util.master_path).decode().strip()
    except Exception:
        return None

def hash_path(path):
    dirhash = {}
    for dirpath, dirnames, filenames in os.walk(path, topdown=False):
        hashes = []
        for filename in filenames:
            filepath = os.path.join(dirpath, filename)
            sha1 = hash_object(util.read_bytefile(filepath), util.filepath_type, write=True)
            hashes.append(sha1)
        for dirname in dirnames:
            hashes.append(dirhash[dirname])
        curdirname = os.path.basename(os.path.normpath(dirpath))
        hash_list = ','.join(hashes)
        sha1 = hash_object(hash_list, util.dirpath_type, write=True)
        dirhash[curdirname] = sha1
    return dirhash[curdirname]

def hash_command(cmd):
    return hash_object(util.runcmd(cmd), util.command_type, write=True)

def hash_variable(var):
    return hash_object(os.getenv(var), util.variable_type, write=True)

def hash_typedvalue(value):
    return hash_object(str(value), type(value).__name__, write=True)

hashingmap = { util.path_type: hash_path,
    util.command_type: hash_command,
    util.variable_type: hash_variable
}
