"""Implement core functions.
"""
from __future__ import absolute_import, division, print_function, unicode_literals
import enum, hashlib, os, stat, json, logging, subprocess
import struct, urllib.request, zlib, configparser

regpath = os.path.join('.closeup', 'register')

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

def read_file(path):
    """Read contents of file at given path as bytes."""
    with open(path, 'rb') as f:
        return f.read()

def write_file(path, data):
    """Write data bytes to file at given path."""
    with open(path, 'wb') as f:
        f.write(data)

def parse_name(name):
    """Split and parse name into namepath."""
    parsed = []
    for item in name.split('/'):
        poslb = item.find('[')
        posrb = item.find(']')
        if poslb<=0 or posrb<=0 or posrb<=poslb or \
            (posrb+1)!=len(item) or not item[poslb+1:posrb].isdigit():
            parsed.append((item, None))
        else:
            parsed.append((item[:poslb], int(item[poslb+1:posrb])))
    reg_name_list = []
    obj_name_list = list(parsed)

    cur_dict = read_register()
    for item_name, index in parsed:
        if item_name not in cur_dict:
            return reg_name_list, obj_name_list
        if index is None:
            cur_dict = cur_dict[item_name]
        else:
            cur_dict = cur_dict[item_name][index]
        reg_name_list.append(obj_name_list.pop(0))
    return reg_name_list, obj_name_list

def is_leaf(e):
    return isinstance(e, list) and len(e)==2 and isinstance(e[0],str) and \
        isinstance(e[1],dict) and 'reg_type' in e[1]

def are_leaves(e):
    return isinstance(e, list) and all(is_leaf(_e) for _e in e)

def get_leaves(e):
    for k, v in e.items():
        if are_leaves(v):
            for _v in v:
                yield _v
        else:
            return get_leaves(v) 

def read_register():
    if os.path.exists(regpath):
        with open(regpath, 'r') as freg:
            return json.load(freg)
    else:
        return {}

def write_register(reg_dict):
    with open(regpath, 'w') as freg:
        json.dump(reg_dict, freg)

def get_register_entry(reg_name_list):
    """Return an item in register."""
    logging.debug('calling get_register_entry({})'.format(reg_name_list))
    cur_container = read_register()
    for item_name, index in reg_name_list:
        if isinstance(index, int):
            cur_container = cur_container[item_name][index]
        else:
            cur_container = cur_container[item_name]
    logging.debug('returning get_register_entry with {}'.format(cur_container))
    return cur_container

def hash_object(data, obj_type, write=True):
    """Compute hash of object data of given type and write to object store if
    "write" is True. Return SHA-1 object hash as hex string.
    """
    header = '{} {}'.format(obj_type, len(data)).encode()
    full_data = header + b'\x00' + data
    sha1 = hashlib.sha1(full_data).hexdigest()
    if write:
        path = os.path.join('.closeup', 'objects', sha1[:2], sha1[2:])
        if not os.path.exists(path):
            os.makedirs(os.path.dirname(path), exist_ok=True)
            write_file(path, zlib.compress(full_data))
    return sha1

def hash_command(command):
    stdout = subprocess.check_output(os.path.expandvars(command).split())
    return hash_object(stdout, 'command')

def hash_file(path):
    return hash_object(b'', 'path')

def hash_variable(var):
    return hash_object(os.path.expandvars('$'+var).encode(), 'variable')

def write_image():
    reg_dict = read_register()
    for item, attr in get_leaves(reg_dict):
        reg_type = attr['reg_type']
        if reg_type == 'path':
            sha1 = hash_file(item)
        elif reg_type == 'command':
            sha1 = hash_command(item)
        elif reg_type == 'variable':
            sha1 = hash_variable(item)
        attr['sha'] = sha1
    write_register(reg_dict)
    return hashlib.sha1(json.dumps(reg_dict, separators=(',',':')).encode()).hexdigest()

def find_object(sha1_prefix):
    """Find object with given SHA-1 prefix and return path to object in object
    store, or raise ValueError if there are no objects or multiple objects
    with this prefix.
    """
    if len(sha1_prefix) < 2:
        raise ValueError('hash prefix must be 2 or more characters')
    obj_dir = os.path.join('.closeup', 'objects', sha1_prefix[:2])
    rest = sha1_prefix[2:]
    objects = [name for name in os.listdir(obj_dir) if name.startswith(rest)]
    if not objects:
        raise ValueError('object {!r} not found'.format(sha1_prefix))
    if len(objects) >= 2:
        raise ValueError('multiple objects ({}) with prefix {!r}'.format(
                len(objects), sha1_prefix))
    return os.path.join(obj_dir, objects[0])


def read_object(sha1_prefix):
    """Read object with given SHA-1 prefix and return tuple of
    (object_type, data_bytes), or raise ValueError if not found.
    """
    path = find_object(sha1_prefix)
    full_data = zlib.decompress(read_file(path))
    nul_index = full_data.index(b'\x00')
    header = full_data[:nul_index]
    obj_type, size_str = header.decode().split()
    size = int(size_str)
    data = full_data[nul_index + 1:]
    assert size == len(data), 'expected size {}, got {} bytes'.format(
            size, len(data))
    return (obj_type, data)


#def get_status():
#    """Get status of working copy, return tuple of (changed_paths, new_paths,
#    deleted_paths).
#    """
#    paths = set()
#    for root, dirs, files in os.walk('.'):
#        dirs[:] = [d for d in dirs if d != '.closeup']
#        for file in files:
#            path = os.path.join(root, file)
#            path = path.replace('\\', '/')
#            if path.startswith('./'):
#                path = path[2:]
#            paths.add(path)
#    entries_by_path = {e.path: e for e in read_register()}
#    entry_paths = set(entries_by_path)
#
#    staged = set()
#    for p in (paths & entry_paths):
#        try:
#            find_object(hash_object(read_file(p), 'blob', write=False))
#        except FileNotFoundError as e:
#            import pdb; pdb.set_trace()
#
#    modified = {p for p in (paths & entry_paths)
#               if hash_object(read_file(p), 'blob', write=False) !=
#                  entries_by_path[p].sha1.hex()}
#    untracted = paths - entry_paths
#    deleted = entry_paths - paths
#    return (sorted(modified), sorted(untracted), sorted(deleted))


def get_local_master_hash():
    """Get current commit hash (SHA-1 string) of local master branch."""
    master_path = os.path.join('.closeup', 'refs', 'heads', 'master')
    try:
        return read_file(master_path).decode().strip()
    except FileNotFoundError:
        return None

def extract_lines(data):
    """Extract list of lines from given server data."""
    lines = []
    i = 0
    for _ in range(1000):
        line_length = int(data[i:i + 4], 16)
        line = data[i + 4:i + line_length]
        lines.append(line)
        if line_length == 0:
            i += 4
        else:
            i += line_length
        if i >= len(data):
            break
    return lines


def build_lines_data(lines):
    """Build byte string from given lines to send to server."""
    result = []
    for line in lines:
        result.append('{:04x}'.format(len(line) + 5).encode())
        result.append(line)
        result.append(b'\n')
    result.append(b'0000')
    return b''.join(result)


def http_request(url, username, password, data=None):
    """Make an authenticated HTTP request to given URL (GET by default, POST
    if "data" is not None).
    """
    password_manager = urllib.request.HTTPPasswordMgrWithDefaultRealm()
    password_manager.add_password(None, url, username, password)
    auth_handler = urllib.request.HTTPBasicAuthHandler(password_manager)
    opener = urllib.request.build_opener(auth_handler)
    f = opener.open(url, data=data)
    return f.read()


def get_remote_master_hash(closeup_url, username, password):
    """Get commit hash of remote master branch, return SHA-1 hex string or
    None if no remote commits.
    """
    url = closeup_url + '/info/refs?service=closeup-receive-pack'
    response = http_request(url, username, password)
    lines = extract_lines(response)
    assert lines[0] == b'# service=closeup-receive-pack\n'
    assert lines[1] == b''
    if lines[2][:40] == b'0' * 40:
        return None
    master_sha1, master_ref = lines[2].split(b'\x00')[0].split()
    assert master_ref == b'refs/heads/master'
    assert len(master_sha1) == 40
    return master_sha1.decode()


def read_image(sha1=None, data=None):
    """Read image object with given SHA-1 (hex string) or data, and return list
    of (mode, path, sha1) tuples.
    """
    if sha1 is not None:
        obj_type, data = read_object(sha1)
        assert obj_type == 'image'
    elif data is None:
        raise TypeError('must specify "sha1" or "data"')
    i = 0
    entries = []
    for _ in range(1000):
        end = data.find(b'\x00', i)
        if end == -1:
            break
        mode_str, path = data[i:end].decode().split()
        mode = int(mode_str, 8)
        digest = data[end + 1:end + 21]
        entries.append((mode, path, digest.hex()))
        i = end + 1 + 20
    return entries


def find_image_objects(image_sha1):
    """Return set of SHA-1 hashes of all objects in this image (recursively),
    including the hash of the image itself.
    """
    objects = {image_sha1}
    for mode, path, sha1 in read_image(sha1=image_sha1):
        if stat.S_ISDIR(mode):
            objects.update(find_image_objects(sha1))
        else:
            objects.add(sha1)
    return objects


def find_commit_objects(commit_sha1):
    """Return set of SHA-1 hashes of all objects in this commit (recursively),
    its tree, its parents, and the hash of the commit itself.
    """
    objects = {commit_sha1}
    obj_type, commit = read_object(commit_sha1)
    assert obj_type == 'commit'
    lines = commit.decode().splitlines()
    tree = next(l[5:45] for l in lines if l.startswith('tree '))
    objects.update(find_tree_objects(tree))
    parents = (l[7:47] for l in lines if l.startswith('parent '))
    for parent in parents:
        objects.update(find_commit_objects(parent))
    return objects


def find_missing_objects(local_sha1, remote_sha1):
    """Return set of SHA-1 hashes of objects in local commit that are missing
    at the remote (based on the given remote commit hash).
    """
    local_objects = find_commit_objects(local_sha1)
    if remote_sha1 is None:
        return local_objects
    remote_objects = find_commit_objects(remote_sha1)
    return local_objects - remote_objects


def encode_pack_object(obj):
    """Encode a single object for a pack file and return bytes (variable-
    length header followed by compressed data bytes).
    """
    obj_type, data = read_object(obj)
    type_num = ObjectType[obj_type].value
    size = len(data)
    byte = (type_num << 4) | (size & 0x0f)
    size >>= 4
    header = []
    while size:
        header.append(byte | 0x80)
        byte = size & 0x7f
        size >>= 7
    header.append(byte)
    return bytes(header) + zlib.compress(data)


def create_pack(objects):
    """Create pack file containing all objects in given given set of SHA-1
    hashes, return data bytes of full pack file.
    """
    header = struct.pack('!4sLL', b'PACK', 2, len(objects))
    body = b''.join(encode_pack_object(o) for o in sorted(objects))
    contents = header + body
    sha1 = hashlib.sha1(contents).digest()
    data = contents + sha1
    return data
