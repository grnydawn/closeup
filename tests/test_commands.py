from context import closeup
import unittest, sys, os, shutil

from contextlib import contextmanager
from io import StringIO

here = os.path.dirname(os.path.realpath(__file__))
proj = os.path.join(here, 'myproj')
prog = os.path.join(here, 'prog/fort/app1')

@contextmanager
def captured_output():
    new_out, new_err = StringIO(), StringIO()
    old_out, old_err = sys.stdout, sys.stderr
    try:
        sys.stdout, sys.stderr = new_out, new_err
        yield sys.stdout, sys.stderr, old_out, old_err
    finally:
        sys.stdout, sys.stderr = old_out, old_err

class TestCommands(unittest.TestCase):

    def _test_clear(self):
        shutil.rmtree(proj, ignore_errors=True)
        self.assertFalse(os.path.exists(proj))

    def _test_init(self):
        self._test_clear()
        os.chdir(here)
        closeup.main(argv=['init', proj])
        os.chdir(proj)
        self.assertTrue(os.path.exists(os.path.join(proj, '.closeup')))

    def _test_register(self):
        self._test_init()
        closeup.main(argv=['register', 'a[2]/app1', prog])
        closeup.main(argv=['register', 'a[1]/cpuinfo', 'cat /proc/cpuinfo', '-t', 'command'])
        closeup.main(argv=['register', 'b[0]/home', 'HOME', '-t', 'variable'])
        with captured_output() as (out, err, stdout, stderr):
            closeup.main(argv=['show', 'a[2]/app1'])
            output = out.getvalue().strip()
            self.assertTrue(output.find(prog)>0)
            closeup.main(argv=['show', 'a[1]/cpuinfo'])
            output = out.getvalue().strip()
            self.assertTrue(output.find('cpuinfo')>0)
            closeup.main(argv=['show', 'b[0]/home'])
            output = out.getvalue().strip()
            self.assertTrue(output.find('HOME')>0)

    def test_record(self):
        self._test_register()
        closeup.main(argv=['record', 'rec1'])
#        with captured_output() as (out, err, stdout, stderr):
        closeup.main(argv=['show', 'rec1'])
#            output = out.getvalue().strip()
#            #stdout.write('>>> {} <<<\n'.format(output))
#            self.assertTrue(output.find('rec1')>0)

if __name__ == '__main__':
    unittest.main()
