# -*- coding: UTF-8 -*-
"""Implement sub commands."""

from __future__ import absolute_import, division, print_function, unicode_literals
import os, time, getpass, logging
from . import util, namepath, jsonfile, filesys, report
logger = logging.getLogger('closeup')

def init(repo):
    """Create directory for repo and initialize .closeup directory."""
    logger.debug('calling init("{}")'.format(repo))
    os.mkdir(repo)
    os.mkdir(os.path.join(repo, '.closeup'))
    for name in [['objects'], ['refs'],['refs','heads'],['refs','albums']]:
        os.mkdir(os.path.join(repo, '.closeup', *name))
    util.write_bytefile(os.path.join(repo, '.closeup', 'HEAD'),
        b'ref: refs/heads/master')
    print('initialized empty repository: {}'.format(repo))

def register(name, items, reg_type, **kwargs):
    """Add all items to closeup register."""
    logger.debug('calling register("{}", {}, "{}", {})'.format(
        name, items, reg_type, kwargs))
    name_obj = namepath.parse(name)
    reg_file = jsonfile.load_register()
    kwargs['reg_type'] = reg_type
    if isinstance(name_obj.path[-1], int):
        value = [['\x00',item, kwargs, None] for item in items]
    else:
        value = ['\x00',items[0], kwargs, None]
    reg_file.add(util.register_type, name_obj, value)
    reg_file.dump()
    print('registered: {}'.format(items))

def snap(name, msg):
    """Record the registered object in an image"""
    logger.debug('calling snap("{}", "{}")'.format(name, msg))
    reg_file = jsonfile.load_register()
    reg_file.hash_object()
    reg_file.dump()
    reg_hash = filesys.hash_object(util.register_type, str(reg_file))
    parent = filesys.get_local_master_hash()
    lines = ['register ' + reg_hash]
    if parent:
        lines.append('parent ' + parent)
    lines.append('recorder ' + getpass.getuser())
    lines.append('datetime ' + util.datetimestr())
    lines.append('message ' + msg)
    data = '\n'.join(lines).encode()
    sha1 = filesys.hash_object(data, 'image')
    util.write_bytefile(util.master_path, (sha1 + '\n').encode())
    album_file = jsonfile.load_album()
    if name=='*':
        name_obj = jsonfile.generate_image_name_object(parent)
    else:
        name_obj = namepath.parse(name)
    album_file.add(util.image_type, name_obj, sha1)
    album_file.dump()
    print('recorded an image to master: {}({:7})'.format(
        namepath.pack(name_obj), sha1))
    return sha1

def show(names):
    """show content of objects according to names or hashes."""
    logger.debug('calling show("{}")'.format(names))
    if not names:
        reg_file = jsonfile.load_register()
        print('\nTop of register contains:\n    {}'.format(reg_file.summary()))
        album_file = jsonfile.load_album()
        print('\nTop of album contains:\n    {}'.format(album_file.summary()))
        return

    for name in names:
        name_obj = namepath.parse(name)
        name_type, content = None, None
        reg_file = jsonfile.load_register()
        name_type, content = reg_file.get(name_obj)
        if name_type is None or content is None:
            album_file = jsonfile.load_album()
            name_type, content = album_file.get(name_obj)
        if name_type is None or content is None:
            name_type, content = filesys.get(name_obj)
        if name_type is not None or content is not None:
            report.show(name, name_type, content)
        else:
            print('"{}" is not found.'.format(name))
