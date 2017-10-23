# -*- coding: UTF-8 -*-
"""Implement sub commands."""

from __future__ import absolute_import, division, print_function, unicode_literals
import getpass
from . import extension as ext, util, system, misc, cas, namespace as ns

def checker(node):
    return misc.is_reglink(node)

def run(name, msg):
    """Snap an image"""
    cwd = system.getcwd()
    repo = misc.get_reporoot(cwd)
    regpath = cas.register_path(repo)
    register = system.load_jsonfile(regpath)
    for node in ns.traverse(register, check=checker):
        objtype = node[1]
        content = node[2]
        node[3] = ext.dump(repo, objtype, content)
    system.dump_jsonfile(regpath, register)
    reghash = cas.hash_object(repo, system.read_bytefile(
        regpath), 'register')
    lines = ['register ' + reghash]
    lines.append('recorder ' + getpass.getuser())
    lines.append('datetime ' + util.datetimestr())
    lines.append('message ' + msg)
    data = util.to_bytes('\n'.join(lines))
    sha1 = cas.hash_object(repo, data, 'image')
    imgpath = cas.image_path(repo)
    image = system.load_jsonfile(imgpath)
    branch = image['HEAD']
    tag = '' # TODO: implement this
    if branch in image:
        head_image = image[branch]
        image[branch] = '{}:{}'.format(sha1,tag)
        image[sha1] = head_image
    else:
        image[branch] = '{}:{}'.format(sha1,tag)
    system.dump_jsonfile(imgpath, image)
