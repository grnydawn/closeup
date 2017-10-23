# -*- coding: UTF-8 -*-
"""Implement sub commands."""

from __future__ import absolute_import, division, print_function, unicode_literals
import os, subprocess, json, sys

pathsep = os.sep

def read_bytefile(path):
    with open(path, 'rb') as f:
        return f.read()

def write_bytefile(path, data):
    with open(path, 'wb') as f:
        f.write(data)

def load_jsonfile(path):
    with open(path, 'r') as f:
        return json.loads(f.read())

def dump_jsonfile(path, data):
    with open(path, 'w') as f:
        f.write(json.dumps(data))

def execute(cmd):
    return subprocess.check_output(os.path.expandvars(cmd).split())

def mkdir(path, *mode):
    os.mkdir(path, *mode)

def makedirs(path, *mode):
    os.makedirs(path, *mode)

def pathjoin(path, *paths):
    return os.path.join(path, *paths)

def expandvars(path):
    return os.path.expandvars(path)

def abspath(path):
    return os.path.abspath(path)

def normpath(path):
    return os.path.normpath(path)

def realpath(path):
    return os.path.realpath(path)

def pathexists(path):
    return os.path.exists(path)

def pathsplit(path):
    return os.path.split(path)

def dirname(path):
    return os.path.dirname(path)

def basename(path):
    return os.path.basename(path)

def isfile(path):
    return os.path.isfile(path)

def getcwd():
    return os.getcwd()

def listdir(path):
    return os.listdir(path)

def pathwalk(path, **kwargs):
    return os.walk(path, **kwargs)

def error_exit(msg):
    print(msg)
    os._exit(1)
