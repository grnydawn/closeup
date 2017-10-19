# -*- coding: UTF-8 -*-
"""Implement sub commands."""

from __future__ import absolute_import, division, print_function, unicode_literals
import os, time, getpass, logging
from . import util, namepath, jsonfile, filesys
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
    album_file.add(util.image_type, name_obj, sha1)
    album_file.dump()
    print('recorded an image to master: {}({:7})'.format(
        namepath.pack(name_obj), sha1))
    return sha1

#def show(names):
#    """show content of objects according to names or hashes."""
#    logging.getLogger('closeup').debug('calling show({})'.format(names))
#    try:
#        for name in names:
#            reg_name, reg_data, remained = structure.register_split_name(name)
#            if remained:
#                # select reader for remained
#                core.show_object(reg_data, remained)
#            else:
#                #import pdb; pdb.set_trace()
#                if reg_name:
#                    core.show_register(reg_name, reg_data)
#                    if structure.is_link(reg_data):
#                        core.show_object(reg_data, remained)
#            image_name, image_hash, remained = structure.image_split_name(name)
#            if image_name and image_hash:
#                core.show_image(image_name, image_hash)
#                #print('image {}: {}'.format(structure.pack_name(image_name), image_hash))
#
#    except exception.NameAlreadyExistError as err:
#        logging.getLogger('closeup').error(err, exc_info=True)
#    finally:
#        pass
#
#def record(name, message):
#    """Record the current state of the register to master with given message.
#    Return hash of record object.
#    """
#    try:
#        reg_hash = core.write_image_body()
#        album_hash = core.hash_file(util.albumpath)
#        parent = core.get_local_master_hash()
#        author = getpass.getuser()
#        timestamp = int(time.mktime(time.localtime()))
#        utc_offset = -time.timezone
#        author_time = '{} {}{:02}{:02}'.format(
#                timestamp,
#                '+' if utc_offset > 0 else '-',
#                abs(utc_offset) // 3600,
#                (abs(utc_offset) // 60) % 60)
#        lines = ['register ' + reg_hash]
#        lines.append('album ' + album_hash)
#        if parent:
#            lines.append('parent ' + parent)
#        lines.append('recorder {} {}'.format(author, author_time))
#        lines.append('message {}'.format(message))
#        data = '\n'.join(lines).encode()
#        sha1 = core.hash_object(data, 'image')
#        album = structure.load_album()
#        album.add(name, sha1)
#        album.dump()
#        master_path = os.path.join('.closeup', 'refs', 'heads', 'master')
#        core.write_file(master_path, (sha1 + '\n').encode())
#        print('recorded an image to master: {}({:7})'.format(name, sha1))
#        return sha1
#    except exception.CloseupNameError as err:
#        logging.getLogger('closeup').error(err, exc_info=True)
#    finally:
#        pass
