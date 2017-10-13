"""Implement sub commands.
"""

import difflib, os, stat, sys, time
from . import core

def init(repo):
    """Create directory for repo and initialize .closeup directory."""
    os.mkdir(repo)
    os.mkdir(os.path.join(repo, '.closeup'))
    for name in ['objects', 'refs', 'refs/heads']:
        os.mkdir(os.path.join(repo, '.closeup', name))
    core.write_file(os.path.join(repo, '.closeup', 'HEAD'), b'ref: refs/heads/master')
    print('initialized empty repository: {}'.format(repo))

def register(name, directions, dir_type, **kwargs):
    """Add all directions to closeup register."""
    name_list = name.split('/')
    reg_dict = core.read_register()
    cur_dict = reg_dict
    for name in name_list[:-1]:
        if name not in cur_dict:
            cur_dict[name] = dict()
        cur_dict = cur_dict[name]
    if name_list[-1] in cur_dict:
        raise ValueError('Use "reregister" command to replace "{}".'.format(name))
    kwargs['reg_type'] = dir_type
    cur_dict[name_list[-1]] = (directions, kwargs)
    core.write_register(reg_dict)

def show(names):
    """show content of objects."""
    for name in names:
        reg_name_list, obj_name_list = core.parse_name(name)
        reg_data, reg_attr = core.get_register_entry(reg_name_list)
        reg_name_str_list = [n for n,i in reg_name_list[:-1]]
        reg_name_str_list.append(reg_name_list[-1][0] if reg_name_list[-1][1] is None \
            else '{}[{}]'.format(*reg_name_list[-1]))
        print('{} "{}" is registered with "{}".'.format(
            reg_attr['reg_type'], '/'.join(reg_name_str_list), reg_data))
        if obj_name_list:
            if True: # if image hash is not provided
                image_string = 'Current'
            obj_data = 'Not implemented yet.'
            print('{} value of "{}" is:\n{}'.format(
                image_string, '/'.join(obj_name_list), obj_data))

def commit(name, message):
    """Record the current state of the register to master with given message.
    Return hash of commit object.
    """
    image = core.write_image()
    parent = core.get_local_master_hash()
    if author is None:
        author = '{} <{}>'.format(
                os.environ['GIT_AUTHOR_NAME'], os.environ['GIT_AUTHOR_EMAIL'])
    timestamp = int(time.mktime(time.localtime()))
    utc_offset = -time.timezone
    author_time = '{} {}{:02}{:02}'.format(
            timestamp,
            '+' if utc_offset > 0 else '-',
            abs(utc_offset) // 3600,
            (abs(utc_offset) // 60) % 60)
    lines = ['image ' + image]
    if parent:
        lines.append('parent ' + parent)
    lines.append('author {} {}'.format(author, author_time))
    lines.append('committer {} {}'.format(author, author_time))
    lines.append('')
    lines.append(message)
    lines.append('')
    data = '\n'.join(lines).encode()
    sha1 = core.hash_object(data, 'commit')
    master_path = os.path.join('.closeup', 'refs', 'heads', 'master')
    core.write_file(master_path, (sha1 + '\n').encode())
    print('committed to master: {:7}'.format(sha1))
    return sha1


def cat_file(mode, sha1_prefix):
    """Write the contents of (or info about) object with given SHA-1 prefix to
    stdout. If mode is 'commit', 'tree', or 'blob', print raw data bytes of
    object. If mode is 'size', print the size of the object. If mode is
    'type', print the type of the object. If mode is 'pretty', print a
    prettified version of the object.
    """
    obj_type, data = core.read_object(sha1_prefix)
    if mode in ['commit', 'tree', 'blob']:
        if obj_type != mode:
            raise ValueError('expected object type {}, got {}'.format(
                    mode, obj_type))
        sys.stdout.buffer.write(data)
    elif mode == 'size':
        print(len(data))
    elif mode == 'type':
        print(obj_type)
    elif mode == 'pretty':
        if obj_type in ['commit', 'blob']:
            sys.stdout.buffer.write(data)
        elif obj_type == 'tree':
            for mode, path, sha1 in core.read_tree(data=data):
                type_str = 'tree' if stat.S_ISDIR(mode) else 'blob'
                print('{:06o} {} {}\t{}'.format(mode, type_str, sha1, path))
        else:
            assert False, 'unhandled object type {!r}'.format(obj_type)
    else:
        raise ValueError('unexpected mode {!r}'.format(mode))


def ls_files(details=False):
    """Print list of files in register (including mode, SHA-1, and stage number
    if "details" is True).
    """
    for entry in read_register():
        if details:
            stage = (entry.flags >> 12) & 3
            print('{:6o} {} {:}\t{}'.format(
                    entry.mode, entry.sha1.hex(), stage, entry.path))
        else:
            print(entry.path)


#def status():
#    """Show status of working copy."""
#    modified, untracted, deleted = get_status()
#    if modified:
#        print('modified files:')
#        for path in modified:
#            print('   ', path)
#    if untracted:
#        print('untracted files:')
#        for path in untracted:
#            print('   ', path)
#    if deleted:
#        print('deleted files:')
#        for path in deleted:
#            print('   ', path)


def diff():
    """Show diff of images changed."""
    modified, _, _ = get_status()
    entries_by_path = {e.path: e for e in read_register()}
    for i, path in enumerate(modified):
        sha1 = entries_by_path[path].sha1.hex()
        obj_type, data = core.read_object(sha1)
        assert obj_type == 'blob'
        register_lines = data.decode().splitlines()
        image_lines = read_file(path).decode().splitlines()
        diff_lines = difflib.unified_diff(
                register_lines, image_lines,
                '{} (register)'.format(path),
                '{} (image)'.format(path),
                lineterm='')
        for line in diff_lines:
            print(line)
        if i < len(modified) - 1:
            print('-' * 70)


def push(closeup_url, username=None, password=None):
    """Push master branch to given closeup repo URL."""
    if username is None:
        username = os.environ['GIT_USERNAME']
    if password is None:
        password = os.environ['GIT_PASSWORD']
    remote_sha1 = core.get_remote_master_hash(closeup_url, username, password)
    local_sha1 = core.get_local_master_hash()
    missing = core.find_missing_objects(local_sha1, remote_sha1)
    print('updating remote master from {} to {} ({} object{})'.format(
            remote_sha1 or 'no commits', local_sha1, len(missing),
            '' if len(missing) == 1 else 's'))
    lines = ['{} {} refs/heads/master\x00 report-status'.format(
            remote_sha1 or ('0' * 40), local_sha1).encode()]
    data = core.build_lines_data(lines) + core.create_pack(missing)
    url = closeup_url + '/closeup-receive-pack'
    response = core.http_request(url, username, password, data=data)
    lines = core.extract_lines(response)
    assert len(lines) >= 2, \
        'expected at least 2 lines, got {}'.format(len(lines))
    assert lines[0] == b'unpack ok\n', \
        "expected line 1 b'unpack ok', got: {}".format(lines[0])
    assert lines[1] == b'ok refs/heads/master\n', \
        "expected line 2 b'ok refs/heads/master\n', got: {}".format(lines[1])
    return (remote_sha1, missing)

