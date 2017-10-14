# -*- coding: UTF-8 -*-
"""Test name split functions.
"""
from __future__ import absolute_import, division, print_function, unicode_literals

from context import closeup
import unittest, sys, os, shutil

here = os.path.dirname(os.path.realpath(__file__))
examples = [
    ('a/b/c/d', [1],),
    ('b/b/c/d/',[2]),
    ('c[0]/b/c/d', [{1:2},1,2]),
    ('d/b/[2]c/d', [[1,2]]),
    ('e/b/c/d[2]', [1,3])
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
