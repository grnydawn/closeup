# -*- coding: UTF-8 -*-
"""Implement report functions."""

from __future__ import absolute_import, division, print_function, unicode_literals
import os
from . import util

def show(name, rpt_type, content):
    lines = [ '"{}" = '.format(name) ]
    if rpt_type==util.image_type:
        lines.append('\n'.join(content))
    elif rpt_type==util.command_type:
        lines.append(content)
    elif rpt_type==util.variable_type:
        lines.append(content)
    elif rpt_type==util.dirpath_type:
        lines.append(content)
        lines.append(' '.join(os.listdir(content)))
    else:
        lines.append('report type "{}" is not supported yet.'.format(rpt_type))
    print('\n'.join(lines))
