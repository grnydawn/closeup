"""Implement closeup command-line interface"""

import sys, argparse
from .commands import ( register, cat_file, commit, diff, hash_object,
    init, ls_files, push )

def main(argv=None):
    parser = argparse.ArgumentParser()
    sub_parsers = parser.add_subparsers(dest='command', metavar='command')
    sub_parsers.required = True

    sub_parser = sub_parsers.add_parser('init',
            help='initialize a new repo')
    sub_parser.add_argument('repo',
            help='directory name for new repo')

    sub_parser = sub_parsers.add_parser('register',
            help='add object(s) to register')
    sub_parser.add_argument('name',
            help='name for objects')
    sub_parser.add_argument('directions', nargs='+', metavar='direction',
            help='direction(s) of objects to register')
    sub_parser.add_argument('-t', choices=['path', 'command', 'variable'],
            default='path', dest='type',
            help='type of object (default %(default)r)')

    sub_parser = sub_parsers.add_parser('cat-file',
            help='display contents of object')
    valid_modes = ['commit', 'tree', 'blob', 'size', 'type', 'pretty']
    sub_parser.add_argument('mode', choices=valid_modes,
            help='object type (commit, tree, blob) or display mode (size, '
                 'type, pretty)')
    sub_parser.add_argument('hash_prefix',
            help='SHA-1 hash (or hash prefix) of object to display')

    sub_parser = sub_parsers.add_parser('commit',
            help='commit current state of register to master branch')
    sub_parser.add_argument('-a', '--author',
            help='commit author in format "A U Thor <author@example.com>" '
                 '(uses GIT_AUTHOR_NAME and GIT_AUTHOR_EMAIL environment '
                 'variables by default)')
    sub_parser.add_argument('-m', '--message', required=True,
            help='text of commit message')

    sub_parser = sub_parsers.add_parser('diff',
            help='show diff of images changed')

    sub_parser = sub_parsers.add_parser('hash-object',
            help='hash contents of given path (and optionally write to '
                 'object store)')
    sub_parser.add_argument('path',
            help='path of file to hash')
    sub_parser.add_argument('-t', choices=['commit', 'tree', 'blob'],
            default='blob', dest='type',
            help='type of object (default %(default)r)')
    sub_parser.add_argument('-w', action='store_true', dest='write',
            help='write object to object store (as well as printing hash)')

    sub_parser = sub_parsers.add_parser('ls-files',
            help='list files in register')
    sub_parser.add_argument('-s', '--stage', action='store_true',
            help='show object details (mode, hash, and stage number) in '
                 'addition to path')

    sub_parser = sub_parsers.add_parser('push',
            help='push master branch to given clouseup server URL')
    sub_parser.add_argument('closeup_url',
            help='URL of closeup repo, eg: https://bytealbum.com/pycloseup.closeup')
    sub_parser.add_argument('-p', '--password',
            help='password to use for authentication (uses GIT_PASSWORD '
                 'environment variable by default)')
    sub_parser.add_argument('-u', '--username',
            help='username to use for authentication (uses GIT_USERNAME '
                 'environment variable by default)')

#    sub_parser = sub_parsers.add_parser('status',
#            help='show status of working copy')

    args = parser.parse_args(args=argv)

    if args.command == 'init':
        init(args.repo)
    elif args.command == 'register':
        register(args.name, args.directions, args.type)
    elif args.command == 'cat-file':
        try:
            cat_file(args.mode, args.hash_prefix)
        except ValueError as error:
            print(error, file=sys.stderr)
            sys.exit(1)
    elif args.command == 'commit':
        commit(args.message, author=args.author)
    elif args.command == 'diff':
        diff()
    elif args.command == 'hash-object':
        sha1 = hash_object(read_file(args.path), args.type, write=args.write)
        print(sha1)
    elif args.command == 'ls-files':
        ls_files(details=args.stage)
    elif args.command == 'push':
        push(args.closeup_url, username=args.username, password=args.password)
#    elif args.command == 'status':
#        status()
    else:
        assert False, 'unexpected command {!r}'.format(args.command)
