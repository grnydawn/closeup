# -*- coding: UTF-8 -*-
"""Implement sub commands."""

from __future__ import absolute_import, division, print_function, unicode_literals
import sys, time, datetime

def to_bytes(s, encoding='utf-8'):
    try:
        return s.encode(encoding)
    except:
        return s

def to_unicodes(s, encoding=None):
    try:
        if encoding is None:
            encoding = sys.stdin.encoding
        return s.decode(encoding)
    except:
        return s

def datetimestr():
    ts = time.time()
    utc = datetime.datetime.utcfromtimestamp(ts)
    now = datetime.datetime.fromtimestamp(ts)
    tzdiff = now - utc
    secdiff = int(tzdiff.days*24*3600 + tzdiff.seconds)
    tzstr = '{0}{1}'.format('+' if secdiff>=0 else '-',
        time.strftime('%H:%M:%S', time.gmtime(abs(secdiff))))
    return '{0} {1}'.format(str(now), tzstr)


