from context import closeup
from closeup import main
import unittest, sys, os, shutil

here = os.path.dirname(os.path.realpath(__file__))
proj = os.path.join(here, 'myproj')
prog = os.path.join(here, 'prog/fort/app1')

#from contextlib import contextmanager
#from io import StringIO
#@contextmanager
#def captured_output():
#    new_out, new_err = StringIO(), StringIO()
#    old_out, old_err = sys.stdout, sys.stderr
#    try:
#        sys.stdout, sys.stderr = new_out, new_err
#        yield sys.stdout, sys.stderr, old_out, old_err
#    finally:
#        sys.stdout, sys.stderr = old_out, old_err

class TestCommands(unittest.TestCase):

    def _test_clear(self):
        shutil.rmtree(proj, ignore_errors=True)
        self.assertFalse(os.path.exists(proj))

    def _test_init(self):
        self._test_clear()
        os.chdir(here)
        main.main(argv=['init', proj])
        os.chdir(proj)
        self.assertTrue(os.path.exists(os.path.join(proj, '.closeup')))

    def _test_register(self):
        self._test_init()
        main.main(argv=['register', 'a[1]/cpuinfo', 'cat /proc/cpuinfo', '-t', 'command'])
        main.main(argv=['register', 'a[2]/app1', prog])
        main.main(argv=['register', 'b[0]/home', 'HOME', '-t', 'variable'])
        main.main(argv=['register', 'b[1]/date', 'date', '-t', 'command'])
        main.main(argv=['register', 'apptest', 'cd {}; make test'.format(prog), '-t', 'action'])

    def _test_snap(self):
        self._test_register()
        main.main(argv=['snap'])

    def _test_record(self):
        self._test_snap()
        main.main(argv=['record', 'apptest'])
        main.main(argv=['record', 'apptest'])

    def test_show(self):
        self._test_record()
        main.main(argv=['show'])
        main.main(argv=['show', 'a'])
        main.main(argv=['show', 'a[0]'])
        main.main(argv=['show', 'a[1]'])
        main.main(argv=['show', 'a[2]'])
        main.main(argv=['show', 'a[1]/cpuinfo'])
        main.main(argv=['show', 'b[1]/date'])
        main.main(argv=['show', 'b[0]/home'])
        main.main(argv=['show', 'a[2]/app1'])
        main.main(argv=['show', 'a[2]/app1/add.f90'])
        main.main(argv=['show', 'HEAD'])
        main.main(argv=['show', 'HEAD~1'])
        main.main(argv=['show', 'apptest'])
        main.main(argv=['show', 'a[2]/app1/add.f90/main/myadd'])

if __name__ == '__main__':
    unittest.main.main()
