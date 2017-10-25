# -*- coding: UTF-8 -*-
"""Implement sub commands."""

from __future__ import absolute_import, division, print_function, unicode_literals
import getpass
from . import (extension as ext, util, system, misc, cas, namespace as ns,
    cmdsnap, error)

REC = '__record__'

def checker(node):
    return misc.is_reglink(node)

def doaction(node, record, msg):
    objtype = node[1]
    content = node[2]
    if objtype=='action':
        try:
            stdout = misc.runcmd(content)
            record.append(cmdsnap.run([], msg))
        except system.CalledProcessError as err:
            record.append(None)

def run(name, msg):
    """Record an image
        A record is as a list in image
    """
    cwd = system.getcwd()
    repo = misc.get_reporoot(cwd)
    regpath = cas.register_path(repo)
    register = system.load_jsonfile(regpath)
    record = [cmdsnap.run([], msg)]
    node = ns.get(register, name)
    if misc.is_reglink(node):
        doaction(node, record, '{:d}:{}'.format(0, msg))
    elif isinstance(node, list) and  \
        all(misc.is_reglink(v) for v in node):
        for idx, v in enumerate(node):
            doaction(v, record, '{:d}:{}'.format(idx, msg))
    else:
        system.error_exit('"{}" is not an correction action.'.format(name))
    imgpath = cas.image_path(repo)
    image = system.load_jsonfile(imgpath)
    if REC not in image:
        image[REC] = {}
    records = image[REC]
    try:
        node = ns.get(records, name)
    except error.NamePathNotFound as err:
        node = []
        ns.set(records, name, node)
    node.append(record)
    system.dump_jsonfile(imgpath, image)
    return  record
