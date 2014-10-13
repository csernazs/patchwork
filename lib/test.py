

import patchwork as pw

import unittest
import tempfile
import os
import shutil

pjoin = os.path.join


class FooError(Exception):
    pass
    
class TempDirMixIn(object):
    def setUp(self):
        self.tempdir = tempfile.mkdtemp()

    def tearDown(self):
        try:
            shutil.rmtree(self.tempdir)
        except OSError: # hmm...
            pass
            

class TestPatch(TempDirMixIn, unittest.TestCase):
    def setUp(self):
        super(TestPatch, self).setUp()
        self.filename = pjoin(self.tempdir, "test.txt")

    def create_testfile(self, name=None):
        if name is None:
            name = self.filename
            
        with open(name, "w") as testfile:
            testfile.write("line1\nline2\nline3\n")

        return name
        
    
    def t_patch(self, p_ctx, input="line1\nline2\nline3\n", output="line4\nline5\nline6\n"):
        i_first, i_rest = input.split("\n", 1)
        i_first = i_first + "\n"

        o_first, o_rest = output.split("\n", 1)
        o_first = o_first + "\n"
        
        with p_ctx as patch:
            self.assertEqual(patch.readline(), i_first)
            self.assertEqual(patch.read(), i_rest)
            patch.write(o_first)
            patch.writelines(o_rest)

        with open(patch.infile.name, "r") as f:
            self.assertEqual(f.read(), output)
        self.assertFalse(os.path.isfile(patch.infile.name+".new"))
        self.assertTrue(os.path.isfile(patch.infile.name+".old"))

        # check backup
        with open(patch.infile.name+".old", "r") as f:
            self.assertTrue(f.read(), input)
            
    def test_100_simple_filename(self):
        self.create_testfile()

        self.t_patch(pw.Patch(self.filename))

    def test_110_simple_fileobject(self):
        self.create_testfile()
        self.t_patch(pw.Patch(open(self.filename)))
            

    def test_120_exception(self):
        self.create_testfile()

        try:
            with pw.Patch(self.filename) as patch:
                self.assertEqual(patch.readline(), "line1\n")
                self.assertEqual(patch.read(), "line2\nline3\n")
                
                # raise exception
                raise FooError("this is normal")
                
                patch.write("line4\n")
                patch.writelines(["line5\n", "line6\n"])
        except FooError:
            pass
        else:
            self.fail("No exception was raised")
        
        
        # file should be untouched
        with open(patch.infile.name, "r") as f:
            self.assertEqual(f.read(), "line1\nline2\nline3\n")
        # there should be no .new file
        self.assertFalse(os.path.isfile(patch.infile.name+".new"))

    def test_130_double(self):
        self.create_testfile()
        
        self.t_patch(pw.Patch(self.filename))
        self.t_patch(pw.Patch(self.filename), input="line4\nline5\nline6\n",  output="line7\nline8\nline9\n")
    


    def test_140_iter(self):
        self.create_testfile()
        
        with pw.Patch(self.filename) as patch:
            for idx, line in enumerate(patch):
                self.assertEqual(line, "line%d\n" % (idx+1))

    def test_140_readlines(self):
        self.create_testfile()
        
        with pw.Patch(self.filename) as patch:
            self.assertEqual(patch.readlines(), ["line1\n", "line2\n", "line3\n"])

    def test_200_invalid_close(self):
        self.create_testfile()
        
        with pw.Patch(self.filename) as patch:
            os.close(patch.infile.fileno())
            os.close(patch.newfile.fileno())
            

    def test_201_commit(self):
        self.create_testfile()
        p = pw.Patch(self.filename)
        for line in p:
            p.write(line[-2]+"\n")
        p.commit()
        with open(self.filename, "r") as f:
            self.assertEqual(f.read(), "1\n2\n3\n")

    def test_201_rollback(self):
        self.create_testfile()
        p = pw.Patch(self.filename)
        for line in p:
            p.write(line[-2]+"\n")
        p.rollback()
        with open(self.filename, "r") as f:
            self.assertEqual(f.read(), "line1\nline2\nline3\n")
        
            
    def test_900_typeerror_1(self):
        with self.assertRaises(TypeError):
            pw.Patch(["foobar"])

if __name__ == "__main__":
    unittest.main()
                






