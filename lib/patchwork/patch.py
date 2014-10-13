

import abc
import os
import six

if six.PY3:
    import io
    file_types = (io.TextIOWrapper,)
else:
    import abc
    file_types = (abc.types.FileType,)

class Patch(object):
    def __init__(self, file, new_suffix=".new", backup_suffix=".old", read_mode="r", write_mode="w", auto_begin=True):
        if not isinstance(file, six.string_types + file_types):
            raise TypeError("file must be string or file object")
            
        self.file = file
        self.new_suffix = new_suffix
        self.backup_suffix = backup_suffix
        self.read_mode = read_mode
        self.write_mode = write_mode
        if auto_begin:
            self.begin()

    def begin(self):
        if isinstance(self.file, six.string_types):
            self.infile = open(self.file, self.read_mode)
        elif isinstance(self.file, file_types):
            self.infile = self.file
            self.write_mode = self.file.mode.replace("r", "w")
        else:
            raise TypeError("file must be string or file object")

        if self.backup_suffix:
            self.backupfile_name = self.infile.name+self.backup_suffix
            if os.path.isfile(self.backupfile_name):
                os.rename(self.backupfile_name, self.infile.name)
            
        newfile_name = self.infile.name + self.new_suffix
        self.newfile = open(newfile_name, self.write_mode)

    def __enter__(self):
        return self
        
    def __iter__(self):
        return self.infile.__iter__()

    def read(self, n=None):
        if n is None:
            return self.infile.read()
        else:
            return self.infile.read(n)

    def readline(self):
        return self.infile.readline()
    
    def readlines(self):
        return self.infile.readlines()

    def write(self, data):
        return self.newfile.write(data)

    def writelines(self, lines):
        return self.newfile.writelines(lines)
        
    def _close_all(self):
        try:
            self.infile.close()
        except IOError:
            pass

        try:
            self.newfile.close()
        except IOError:
            pass
        
    def close(self):
        self.commit()
        
    def commit(self):
        self._close_all()
        
        # if backup is set, make a backup
        if self.backup_suffix:
            os.rename(self.infile.name, self.backupfile_name)
        
        # move the new file to the orig
        # this should be atomic on POSIX
        os.rename(self.newfile.name, self.infile.name)

    def rollback(self):
        self._close_all()
        os.unlink(self.newfile.name)
        
    def __exit__(self, exc_type, exc_value, traceback):
        if exc_type: # exception was raised, ignore the new file
            self.rollback()
        else: # no exception, commit
            self.commit()
            
