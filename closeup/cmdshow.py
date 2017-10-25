# -*- coding: UTF-8 -*-
"""Implement sub commands."""

from __future__ import absolute_import, division, print_function, unicode_literals
from . import system, misc, cas, namespace as ns, error, extension as ext, util

def run(names):
    cwd = system.getcwd()
    repo = misc.get_reporoot(cwd)
    regpath = cas.register_path(repo)
    register = system.load_jsonfile(regpath)
    imgpath = cas.image_path(repo)
    image = system.load_jsonfile(imgpath)
    if names:
        for name in names:
            if not name: continue
            try:
                regvalue = ns.get(register, name)
                if misc.is_reglink(regvalue):
                    print('{}:"{}"'.format(regvalue[1], regvalue[2]))
                else:
                    if isinstance(regvalue, list):
                        if len(regvalue)>5:
                            print('[0], [1], ..., [{}]'.format(len(regvalue)-1))
                        else:
                            print(', '.join(['[{:d}]'.format(i) for i in range(len(regvalue))]))
                    elif isinstance(regvalue, dict):
                        print(' '.join([system.pathsep+k for k in regvalue.keys()]))
                    else:
                        print(regvalue)
                continue
            except error.PathTypeMismatch as err:
                if misc.is_reglink(err.node):
                    summary = ext.summary(repo, err.node[1], err.node[2],
                        extra=err.nextpath)
                    print(summary)
                    continue
                else:
                    system.error_exit('"{}" is not found.'.format(name))
            except error.NamePathNotFound as err:
                pass

            try:
                if name.startswith('HEAD'):
                    branch = image['HEAD']
                    sha1, tags = image[branch].split(':')
                    rem = name[4:]
                    if len(rem)>1 and rem[0]=='~' and rem[1:].isdigit():
                        anc = int(rem[1:])
                        while anc > 0 :
                            try:
                                sha1, tags = image[sha1].split(':')
                            except KeyError as kerr:
                                break
                            anc -= 1
                    objtype, data = cas.read_object(repo, sha1)
                    if objtype=='image':
                        print(util.to_unicodes(data))
                    continue
                else:
                    system.error_exit('"{}" is not found.'.format(name))
            except error.NamePathNotFound as err:
                continue
            system.error_exit('"{}" is not found.'.format(name))
    else:
        print(' '.join([system.pathsep+k for k in register.keys()]))
        #print(('{} '.format(system.pathsep)).join( register.keys()))
    #import pdb; pdb.set_trace()

