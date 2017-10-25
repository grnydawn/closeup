# -*- coding: UTF-8 -*-
"""Implement register sub commands."""

from __future__ import absolute_import, division, print_function, unicode_literals
from . import logger, system, misc, namespace, cas

def run(regname, targets, regtype):
    """Add all items to closeup register."""
    logger.debug('calling register("{}", {}, "{}")'.format(
        regname, targets, regtype))
    cwd = system.getcwd()
    repo = misc.get_reporoot(cwd)
    regpath = cas.register_path(repo)
    register = system.load_jsonfile(regpath)
    regitems = [['\x00',regtype, t, None] for t in targets]
    if len(regitems)==1:
        namespace.set(register, regname, regitems[0])
    else:
        namespace.set(register, regname, regitems)
    system.dump_jsonfile(regpath, register)
    print('{}:"{}" is registered successfully.'.format(regtype, ', '.join(targets)))

