# -*- coding: UTF-8 -*-
"""Implement sub commands."""

from __future__ import absolute_import, division, print_function, unicode_literals
import getpass
from . import extension as ext, util, system, misc, cas, namespace

def checker(node):
    if isinstance(node, list) and len(node)==4 and node[0]=='\x00':
        return True
    return False

def run(name, msg):
    """Snap an image"""
    cwd = system.getcwd()
    repo = misc.get_reporoot(cwd)
    regpath = cas.register_path(repo)
    register = system.load_jsonfile(regpath)
    for node in namespace.traverse(register, check=checker):
        objtype = node[1]
        content = node[2]
        node[3] = ext.dump(objtype, content)
    system.dump_jsonfile(regpath, register)
    reghash = cas.hash_object(util.to_bytes(
        str(register)), 'register')
    lines = ['register ' + reghash]
    lines.append('recorder ' + getpass.getuser())
    lines.append('datetime ' + util.datetimestr())
    lines.append('message ' + msg)
    data = util.to_bytes('\n'.join(lines))
    sha1 = cas.hash_object(data, 'image')
    imgpath = cas.image_path(repo)
    image = system.load_jsonfile(imgpath)
    branch = image['head']
    if branch in image:
        head_image = image[branch]
        image[branch] = sha1
        image[sha1] = image[head_image]
    else:
        image[branch] = sha1
    system.dump_jsonfile(imgpath, image)
