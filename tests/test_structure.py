# -*- coding: UTF-8 -*-
"""Test name split functions.
"""
from __future__ import absolute_import, division, print_function, unicode_literals

from context import closeup
import unittest, sys, os, shutil

here = os.path.dirname(os.path.realpath(__file__))
examples = [
    ('a/b/c/d[0]', ['\x00', 1, {'reg_type': 'ttt'}]),
    ('b/b[2]/c/e[1]', ['\x00', 1, {'reg_type': 'ttt'}]),
    ('c/b/c/d[2]', ['\x00', 1, {'reg_type': 'ttt'}]),
    ('d/b/c[2]/d[2]', ['\x00', 1, {'reg_type': 'ttt'}]),
]

class TestCommands(unittest.TestCase):

    def test_Name(self):
        for text, value in examples:
            print(str(closeup.Name(text)))

    def test_register(self):
        myreg = os.path.join(here, 'myreg')
        try:
            os.remove(myreg)
        except:
            pass
        #shutil.rmtree(myreg, ignore_errors=True)
        attr = {1:2}
        reg = closeup.Register(myreg)
        for text, value in examples:
            reg.add(text, value, attr)
            self.assertEqual(tuple((v,attr) for v in value),
                tuple((v,a) for s,v,a in reg.get(text) if s=='\x00'))
        reg.dump()
        os.remove(myreg)
        reg = closeup.Register(myreg)
        for text, value in examples:
            reg.add(text, value, attr)
            reg.remove(text)
        reg.dump()

if __name__ == '__main__':
    unittest.main()
