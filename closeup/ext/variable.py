import os

def dump(cup, var, extra):
    return cup.write_text(os.getenv(var))

def summary(cup, var, extra):
    return os.getenv(var)

