"""Implement utility functions.
"""
from __future__ import absolute_import, division, print_function, unicode_literals
import os, sys

regpath = os.path.join('.closeup', 'register')
albumpath = os.path.join('.closeup', 'album')

#class ObjectType(enum.Enum):
#    """Object type enum."""
#    path    = enum.auto()
#    command     = enum.auto()
#    variable    = enum.auto()
#    namepath    = enum.auto()
#    file        = enum.auto()
#    directory   = enum.auto()
#    blob        = enum.auto()
#    string      = enum.auto()
#    integer     = enum.auto() 
#    float       = enum.auto() 
#    boolean     = enum.auto() 
#    datetime    = enum.auto() 
#    null        = enum.auto()

def read_bytefile(path):
    """Read contents of file at given path as bytes."""
    with open(path, 'rb') as f:
        return f.read()

def write_bytefile(path, data):
    """Write data bytes to file at given path."""
    with open(path, 'wb') as f:
        f.write(data)

def cmd_arg(text):
    try:
        return text.decode(sys.getfilesystemencoding())
    except:
        return text

