#!/usr/bin/env python

from setuptools import setup

setup(name="patchwork",
      version="0.1",
      license="MIT",
      description="Python module for patching text files",
      long_description=open("README.rst", "r").read(),
      author="Zsolt Cserna",
      author_email="cserna.zsolt@gmail.com",
      url="http://www.github.com/csernazs/patchwork",
      test_suite="test",
      packages=["patchwork"],
      package_dir={"": "lib"},
      install_requires=["six"],
      keywords=["patch", "patching"],
      classifiers=[
                "Development Status :: 3 - Alpha",
                "Intended Audience :: Developers",
                "Intended Audience :: System Administrators",
                "License :: OSI Approved :: MIT License",
                "Operating System :: OS Independent",
                "Programming Language :: Python :: 2",
                "Programming Language :: Python :: 3",
                ],
     )
     
     