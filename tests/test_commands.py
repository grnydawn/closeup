from context import closeup
import unittest, sys, os, shutil

from contextlib import contextmanager
from io import StringIO

proj = os.path.join(os.path.dirname(__file__), 'myproj')
prog = os.path.join(os.path.dirname(__file__), 'prog/fort/app1')

@contextmanager
def captured_output():
    new_out, new_err = StringIO(), StringIO()
    old_out, old_err = sys.stdout, sys.stderr
    try:
        sys.stdout, sys.stderr = new_out, new_err
        yield sys.stdout, sys.stderr
    finally:
        sys.stdout, sys.stderr = old_out, old_err

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
        closeup.main(argv=['register', 'cpuinfo', 'cat /proc/cpuinfo', '-t', 'command'])
        closeup.main(argv=['register', 'home', 'HOME', '-t', 'variable'])
        with captured_output() as (out, err):
            closeup.main(argv=['show', 'app1'])
            output = out.getvalue().strip()
            self.assertTrue(output.find(prog)>0)
            closeup.main(argv=['show', 'cpuinfo'])
            output = out.getvalue().strip()
            self.assertTrue(output.find('cpuinfo')>0)
            closeup.main(argv=['show', 'home'])
            output = out.getvalue().strip()
            self.assertTrue(output.find('HOME')>0)

if __name__ == '__main__':
    unittest.main()
