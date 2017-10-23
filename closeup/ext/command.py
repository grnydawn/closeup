import os, subprocess

def runcmd(cmd):
    return subprocess.check_output(os.path.expandvars(cmd).split())

def dump(cup, cmd, extra):
    return cup.write_text(runcmd(cmd))

def summary(cup, cmd, extra):
    return runcmd(cmd)

