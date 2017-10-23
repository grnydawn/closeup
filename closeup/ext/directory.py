import os

def dump(cup, path, extra):
    fileext, filecup = cup.get_ext_by_type('file')
    fullpath = os.path.join(path, *extra)
    if os.path.isdir(fullpath):
        dirhash = {}
        for curdir, subdirs, filenames in os.walk(fullpath, topdown=False):
            hashes = []
            for filename in filenames:
                filepath = os.path.join(curdir, filename)
                hashes.append(fileext.dump(filecup, filepath, []))
            for subdir in subdirs:
                if subdir in dirhash:
                    hashes.append(dirhash[subdir])
            curdirname = os.path.basename(os.path.normpath(curdir))
            if hashes:
                hash_list = ','.join(hashes)
                sha1 = cup.write_text(hash_list)
                dirhash[curdirname] = sha1
        return dirhash[curdirname]

    elif os.path.isfile(fullpath):
        return fileext.dump(filecup, filepath, [])
    else:
        for idx in reversed(range(len(extra))):
            objpath = os.path.join(path, *extra[:idx+1])
            remained = extra[idx+1:]
            if os.path.isfile(objpath):
                return fileext.dump(filecup, objpath, remained)
        return 'Can not dump {}:{} at directory.'.format(path, extra)

def summary(cup, path, extra):
    fileext, filecup = cup.get_ext_by_type('file')
    fullpath = os.path.join(path, *extra)
    if os.path.isdir(fullpath):
        return fullpath
    elif os.path.isfile(fullpath):
        return fileext.summary(filecup, filepath, [])
    else:
        for idx in reversed(range(len(extra))):
            objpath = os.path.join(path, *extra[:idx+1])
            remained = extra[idx+1:]
            if os.path.isfile(objpath):
                return fileext.summary(filecup, objpath, remained)
        return 'Can not summary {}:{} at directory.'.format(path, extra)
