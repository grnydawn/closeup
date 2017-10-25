# -*- coding: UTF-8 -*-
"""Implement sub commands."""

from __future__ import absolute_import, division, print_function, unicode_literals
import sys
from . import system, cas, util

here = system.dirname(system.realpath(__file__))
builtin = system.pathjoin(here, 'ext')
extroots = [ builtin ]
cache = {}

class CUPExtInterface(object):
    def __init__(self, repo, objtype):
        self.repo = repo # TODO may hide this to exts
        self.objtype = objtype

    def write_text(self, text):
        return cas.hash_object(self.repo, util.to_bytes(text), self.objtype)

    def get_ext_by_type(self, objtype):
        agent = CUPExtInterface(self.repo, objtype)
        #update_cache(objtype)
        return cache[objtype], agent

    def get_exts_by_file(self, filepath):
        with open(filepath, 'r') as f:
            content = f.read()
        exts = []
        for objtype, ext in cache.items():
            if objtype!=self.objtype and 'parse' in dir(ext):
                try:
                    agent = CUPExtInterface(self.repo, objtype)
                    if ext.parse(agent, content, []):
                        exts.append(ext, agent)
                except Exception as err:
                    print(err)
        return exts

def has_object_type(objtype):
    #update_cache(objtype)
    return objtype in cache

#def update_cache(objtype):
#    # from builtin, user-local, system, remotes
#    if objtype in cache:
#        return
#    namepath = objtype.split(system.pathsep)
#    for idx in range(len(namepath)):
#        for extroot in extroots:
#            reldir = system.pathsep.join(namepath[:idx+1])
#            relpath = reldir+'.py'
#            modpath = system.pathjoin(extroot, relpath)
#            if system.isfile(modpath):
#                sys.path.insert(0, system.dirname(modpath))
#                mod = __import__(namepath[idx], globals(),
#                    locals(), [], 0)
#                cache[reldir] = mod
#                del sys.path[0]

def dump(repo, objtype, content, extra=[]):
    agent = CUPExtInterface(repo, objtype)
    #update_cache(objtype)
    try:
        return cache[objtype].dump(agent, content, extra)
    except Exception as err:
        print(err)
        raise

def summary(repo, objtype, content, extra=[]):
    agent = CUPExtInterface(repo, objtype)
    #update_cache(objtype)
    try:
        return cache[objtype].summary(agent, content, extra)
    except Exception as err:
        print(err)
        raise

def update_cache():
    for extroot in extroots:
        for curdir, subdirs, files in system.pathwalk(extroot):
            for f in files:
                modname, ext = system.splitext(f)
                if ext.endswith('.py'):
                    relpath = system.relpath(curdir, extroot)
                    objtype = system.normpath(system.pathjoin(
                        relpath, modname))
                    sys.path.insert(0, curdir)
                    mod = __import__(modname, globals(),
                        locals(), [], 0)
                    cache[objtype] = mod
                    del sys.path[0]
update_cache()






