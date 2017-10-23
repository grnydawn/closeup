# -*- coding: UTF-8 -*-
"""Implement sub commands."""

from __future__ import absolute_import, division, print_function, unicode_literals
from . import system, misc, cas, namespace as ns, error, extension as ext

def run(names):
    cwd = system.getcwd()
    repo = misc.get_reporoot(cwd)
    regpath = cas.register_path(repo)
    register = system.load_jsonfile(regpath)
    imgpath = cas.image_path(repo)
    image = system.load_jsonfile(imgpath)
    if names:
        for name in names:
            #print('summary of "{}":'.format(name))
            try:
                regvalue = ns.get(register, name)
                if misc.is_reglink(regvalue):
                    summary = ext.summary(repo, regvalue[1], regvalue[2])
                    print(summary)
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
                    raise
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
                        print(objtype, data)
                    continue
                elif not rem:
                    print('CC')
                    import pdb; pdb.set_trace()
            except error.NamePathNotFound as err:
                continue
            system.error_exit('"{}" is not found.'.format(name))
    else:
        print('register top names: {}'.format(', '.join(register.keys())))
        print('current branch: {}'.format(image['HEAD']))
    #import pdb; pdb.set_trace()

