import unittest
from yawinpty import *

class YawinptyTest(unittest.TestCase):
    """tests for yawinpty"""
    def test_helloworld(self):
        """test simple use"""
        pty = Pty(Config(Config.flag.plain_output))
        cfg = SpawnConfig(SpawnConfig.flag.auto_shutdown, cmdline = r'python tests\helloworld.py')
        with open(pty.conout_name(), 'r') as fout:
            pty.spawn(cfg)
            out = fout.read()
        self.assertEqual(out, 'helloworld\n')
    def test_errors(self):
        """test Error classes inherit"""
        for code in range(1, 9):
            err_type = WinptyError._from_code(code)
            err_inst = err_type('awd')
            self.assertTrue(issubclass(err_type, WinptyError))
            self.assertIsInstance(err_inst, WinptyError)
            self.assertIsInstance(err_inst, err_type)
            self.assertEqual(err_inst.code, code)
            self.assertEqual(err_inst.args[0], 'awd')
    def test_echo(self):
        """test echo (IO)"""
        pty = Pty(Config(Config.flag.plain_output))
        pty.spawn(SpawnConfig(SpawnConfig.flag.auto_shutdown, cmdline = r'python tests\echo.py'))
        exc = []
        with open(pty.conin_name(), 'w') as fin:
            for i in range(32):
                tmp = []
                for j in range(i):
                    st = str(j)
                    tmp.append(st)
                    fin.write(st)
                fin.write('\n')
                exc += [''.join(tmp)] * 2
            fin.write('\x1a\n')
        with open(pty.conout_name(), 'r') as fout:
            out = fout.read()
        exc += ['^Z', '']
        print(out)
        self.assertEqual('\n'.join(exc), out)

if __name__ == '__main__':
    unittest.main()
