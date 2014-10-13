[![Build Status](https://travis-ci.org/csernazs/patchwork.svg?branch=master)](https://travis-ci.org/csernazs/patchwork)

patchwork
=========

Effortless atomic file patching.

This package implements the `Patch` class which has very similar methods to
the standard file objects (such as read and write) but instead of using a
single file for reading and writing, it creates a new file to write the
content into.

By this methodology, files can be patched atomically as at the end of the
processing a rename() call will be called in order to rename the new file to
the old file, which replaces its content atomically.  Rename is either
successful or not but it won't leave corrupted files behind.

As an extra, the library offers making backups so you are no more need to
worry about the old content. When you are using the library you can be
ensured that you are working on the original content and you need to focus
on the new content. No more patching incompletely patched files.

The API is dead simple:

```python


from patchwork import Patch

# this opens the file specified ("a.txt") or "a.txt.old" which was created
# by a previous patching as backup

# it also opens "a.txt.new" filename for writing

with Patch("a.txt") as f:
    for line in f:                              # reads form the input file ("a.txt")
        if line.startswith("a"):
            f.write("b"+line[1:])               # writes to the new file ("a.txt.new")
        else:
            f.write(line)

# by exiting the with context, it will rename "a.txt.new" to "a.txt", and
# create "a.txt.old" which will have the original content

# if an unhandled exception was raised within the with block, "a.txt.new" will be
# removed and "a.txt" will be intact

```

In case you don't want to use the with context, you can run the commit() or
close() methods to commit the changes or the rollback() method which keeps
the input file intact while dropping your changes made to the new file.

```python

try:
    patch = Patch("a.txt") # open a.txt, create a.txt.new where new content will be written
    for line in patch:
        if line.startswith("foobar"):
            patch.write("foobar was here") # replace all lines starting with "foobar"
except:
    patch.rollback() # roll back the changes
else:
    patch.commit() # commit the changes

```

