import os, subprocess

def dump(cup, path, extra):
    fullpath = os.path.join(path, *extra)
    if os.path.isfile(fullpath):
        exts = cup.get_exts_by_file(fullpath)
        if exts:
            # TODO: choose one of them
            fileext, filecup = exts[0]
            return fileext.dump(filecup, fullpath, [])
        else:
            with open(path, 'rb') as f:
                return cup.write_text(f.read())
    else:
        for idx in reversed(range(len(extra))):
            objpath = os.path.join(path, *extra[:idx+1])
            remained = extra[idx+1:]
            if os.path.isfile(objpath):
                exts = cup.get_exts_by_file(objpath)
                if exts:
                    # TODO: choose one of them
                    fileext, filecup = exts[0]
                    return fileext.dump(filecup, objpath, remained)
        return 'file: can not dump {}:{}.'.format(path, extra)

def summary(cup, path, extra):
    fullpath = os.path.join(path, *extra)
    if os.path.isfile(fullpath):
        exts = cup.get_exts_by_file(fullpath)
        if exts:
            # TODO: choose one of them
            fileext, filecup = exts[0]
            return fileext.summary(filecup, fullpath, [])
        else:
            return('{}'.format(subprocess.check_output(["ls", fullpath, "-lrt"]).strip()))
    else:
        for idx in reversed(range(len(extra))):
            objpath = os.path.join(path, *extra[:idx+1])
            remained = extra[idx+1:]
            if os.path.isfile(objpath):
                exts = cup.get_exts_by_file(objpath)
                if exts:
                    # TODO: choose one of them
                    fileext, filecup = exts[0]
                    return fileext.summary(filecup, objpath, remained)
        return '{}{}'.format(os.sep, os.sep.join(extra))
