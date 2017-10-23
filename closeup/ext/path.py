import os

def dump(cup, path, extra):
    fullpath = os.path.join(path, *extra)
    if os.path.isdir(fullpath):
        dirext, dircup = cup.get_ext_by_type('directory')
        return dirext.dump(dircup, fullpath, [])
    elif os.path.isfile(fullpath):
        fileext, filecup = cup.get_ext_by_type('file')
        return fileext.dump(filecup, fullpath, [])
    else:
        for idx in reversed(range(len(extra))):
            objpath = os.path.join(path, *extra[:idx+1])
            remained = extra[idx+1:]
            if os.path.isdir(objpath):
                dirext, dircup = cup.get_ext_by_type('directory')
                return dirext.dump(dircup, objpath, remained)
            elif os.path.isfile(objpath):
                fileext, filecup = cup.get_ext_by_type('file')
                return fileext.dump(filecup, objpath, remained)
    return 'Can not dump {}:{} at path.'.format(path, extra)

def summary(cup, path, extra):
    fullpath = os.path.join(path, *extra)
    if os.path.isdir(fullpath):
        dirext, dircup = cup.get_ext_by_type('directory')
        return dirext.summary(dircup, fullpath, [])
    elif os.path.isfile(fullpath):
        fileext, filecup = cup.get_ext_by_type('file')
        return fileext.summary(filecup, fullpath, [])
    else:
        for idx in reversed(range(len(extra))):
            objpath = os.path.join(path, *extra[:idx+1])
            remained = extra[idx+1:]
            if os.path.isdir(objpath):
                dirext, dircup = cup.get_ext_by_type('directory')
                return dirext.summary(dircup, objpath, remained)
            elif os.path.isfile(objpath):
                fileext, filecup = cup.get_ext_by_type('file')
                return fileext.summary(filecup, objpath, remained)
    return 'Can not summarize {}:{} at path.'.format(path, extra)


