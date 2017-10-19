"""Implement utility functions.
"""
from __future__ import absolute_import, division, print_function, unicode_literals
import os, sys, json, logging.config, time, datetime, subprocess

name_delimiter = '/'

# paths to internal files
master_path = os.path.join('.closeup', 'refs', 'heads', 'master')
album_path = os.path.join('.closeup', 'refs', 'albums', 'master')
register_path = os.path.join('.closeup', 'register')

# name types
register_type = 'register'
image_type = 'image'
group_type = 'group'

# registration types
path_type = 'path'
filepath_type = 'file'
dirpath_type = 'directory'
command_type = 'command'
variable_type = 'variable'

# misc. types
nametree_type = 'nametree'

def setup_logging( default_path='logging.json',
    default_level=logging.INFO, env_key='LOG_CFG'):
    """Setup logging configuration
    """
    path = default_path
    value = os.getenv(env_key, None)
    if value:
        path = value
    if os.path.exists(path):
        with open(path, 'rt') as f:
            config = json.load(f)
        logging.config.dictConfig(config)
    else:
        logging.basicConfig(level=default_level)

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
    """Set proper type for command-line arguments."""
    try:
        return text.decode(sys.getfilesystemencoding())
    except:
        return text

def datetimestr():
    ts = time.time()
    utc = datetime.datetime.utcfromtimestamp(ts)
    now = datetime.datetime.fromtimestamp(ts)
    tzdiff = now - utc
    secdiff = int(tzdiff.days*24*3600 + tzdiff.seconds)
    tzstr = '{0}{1}'.format('+' if secdiff>=0 else '-',
        time.strftime('%H:%M:%S', time.gmtime(abs(secdiff))))
    return '{0} {1}'.format(str(now), tzstr)


def runcmd(cmd):
    return subprocess.check_output(os.path.expandvars(cmd).split())
