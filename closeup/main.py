# -*- coding: UTF-8 -*-
"""Implement closeup command-line interface"""

from __future__ import absolute_import, division, print_function, unicode_literals
import os
from argparse import ArgumentParser
from . import commands, util

def main(argv=None):
    """Entry to closeup
    argv is mainly for testing.
    """
    parser = ArgumentParser()
    sub_parsers = parser.add_subparsers(dest='command', metavar='command')
    sub_parsers.required = True

    sub_parser = sub_parsers.add_parser('init',
            help='initialize a new repo')
    sub_parser.add_argument('repo', type=util.cmd_arg,
            help='directory name for new repo')

    sub_parser = sub_parsers.add_parser('register',
            help='add method(s) to register')
    sub_parser.add_argument('name', type=util.cmd_arg,
            help='name for method')
    sub_parser.add_argument('methods', nargs='+', metavar='method',
            help='method(s) to register', type=util.cmd_arg)
    sub_parser.add_argument('-t', choices=[util.path_type,
            util.command_type, util.variable_type],
            default=util.path_type, dest='type',
            help='type of object (default %(default)r)')

    sub_parser = sub_parsers.add_parser('snap',
            help='record current state of the registered')
    sub_parser.add_argument('name', type=util.cmd_arg,
            help='name for image')
    sub_parser.add_argument('-m', '--message',
            default='captured at {}.'.format(util.datetimestr()),
            help='text of commit message')

    sub_parser = sub_parsers.add_parser('show',
            help='show content of name')
    sub_parser.add_argument('names', nargs='+', metavar='name',
            help='name(s) for objects', type=util.cmd_arg)
#
#    sub_parser = sub_parsers.add_parser('cat-file',
#            help='display contents of object')
#    valid_modes = ['commit', 'tree', 'blob', 'size', 'type', 'pretty']
#    sub_parser.add_argument('mode', choices=valid_modes,
#            help='object type (commit, tree, blob) or display mode (size, '
#                 'type, pretty)')
#    sub_parser.add_argument('hash_prefix',
#            help='SHA-1 hash (or hash prefix) of object to display')
#
#    sub_parser = sub_parsers.add_parser('diff',
#            help='show diff of images changed')
#
#    sub_parser = sub_parsers.add_parser('hash-object',
#            help='hash contents of given path (and optionally write to '
#                 'object store)')
#    sub_parser.add_argument('path',
#            help='path of file to hash')
#    sub_parser.add_argument('-t', choices=['commit', 'tree', 'blob'],
#            default='blob', dest='type',
#            help='type of object (default %(default)r)')
#    sub_parser.add_argument('-w', action='store_true', dest='write',
#            help='write object to object store (as well as printing hash)')
#
#    sub_parser = sub_parsers.add_parser('ls-files',
#            help='list files in register')
#    sub_parser.add_argument('-s', '--stage', action='store_true',
#            help='show object details (mode, hash, and stage number) in '
#                 'addition to path')
#
#    sub_parser = sub_parsers.add_parser('push',
#            help='push master branch to given clouseup server URL')
#    sub_parser.add_argument('closeup_url',
#            help='URL of closeup repo, eg: https://bytealbum.com/pycloseup.closeup')
#    sub_parser.add_argument('-p', '--password',
#            help='password to use for authentication (uses GIT_PASSWORD '
#                 'environment variable by default)')
#    sub_parser.add_argument('-u', '--username',
#            help='username to use for authentication (uses GIT_USERNAME '
#                 'environment variable by default)')

#    sub_parser = sub_parsers.add_parser('status',
#            help='show status of working copy')

    args = parser.parse_args(args=argv)

    util.setup_logging(default_path=os.path.join(os.path.dirname(__file__), 'logging.json'))

    # TODO: try except for handling common exception among commands
    process_commands(args)


def process_commands(args):
    """main routine to drive commands"""

    # TODO: try except for handling specific exceptions for each commands
    if args.command == 'init':
        commands.init(args.repo)
    elif args.command == 'register':
        commands.register(args.name, args.methods, args.type)
    elif args.command == 'show':
        commands.show(args.names)
    elif args.command == 'snap':
        commands.snap(args.name, args.message)
#    elif args.command == 'cat-file':
#        try:
#            commands.cat_file(args.mode, args.hash_prefix)
#        except ValueError as err:
#            logging.getLogger('closeup').error(err, exc_info=True)
#            sys.exit(1)
#    elif args.command == 'diff':
#        commands.diff()
#    elif args.command == 'hash-object':
#        sha1 = commands.hash_object(read_file(args.path), args.type, write=args.write)
#        print(sha1)
#    elif args.command == 'ls-files':
#        commands.ls_files(details=args.stage)
#    elif args.command == 'push':
#        commands.push(args.closeup_url, username=args.username, password=args.password)
#    elif args.command == 'status':
#        status()
    else:
        print('ERROR: unexpected command {!r}'.format(args.command))
