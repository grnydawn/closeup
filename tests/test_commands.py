from context import closeup
import unittest
import os
import shutil

proj = os.path.join(os.path.dirname(__file__), 'myproj')
prog = os.path.join(os.path.dirname(__file__), 'prog/fort/app1')

class TestCommands(unittest.TestCase):

    def test_clear(self):
        shutil.rmtree(proj, ignore_errors=True)
        self.assertFalse(os.path.exists(proj))

    def test_init(self):
        self.test_clear()
        os.chdir(os.path.expanduser('~'))
        closeup.main(argv=['init', proj])
        os.chdir(proj)
        self.assertTrue(os.path.exists(os.path.join(proj, '.closeup')))

    def test_register(self):
        self.test_init()
        closeup.main(argv=['register', 'app1', prog])
        #self.assertTrue(os.path.exists(os.path.join(proj, '.closeup')))
        
if __name__ == '__main__':
    unittest.main()
