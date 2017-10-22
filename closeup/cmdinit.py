# -*- coding: UTF-8 -*-
"""Implement sub commands."""

from __future__ import absolute_import, division, print_function, unicode_literals
from . import system, cas, logger

def run(repo):
    """Create directory for repo and initialize .closeup directory."""
    logger.debug('calling init("{}")'.format(repo))
    system.makedirs(cas.objects_path(repo))
    system.dump_jsonfile(cas.register_path(repo), {})
    system.dump_jsonfile(cas.image_path(repo), {'head':'master'})
    print('initialized empty repository: {}'.format(repo))
