#!/usr/bin/env python
"""Setup."""

import imp
import sys

from setuptools import setup, find_packages

if sys.version_info < (3, 6):
    sys.exit("Sorry, Python < 3.6 is not supported")

# read the contents of the README file
with open("README.rst", encoding="utf-8") as f:
    README = f.read()

VERSION = imp.load_source("", "dcrawls.version.py").__version__

print(find_packages)

setup(
    name="dcrawls",
    author="Hugo Dictus",
    author_email="hugo.dictus@epfl.ch",
    version=VERSION,
    description="Visual cortex analyses",
    long_description=README,
    long_description_content_type="text/x-rst",
    license="MIT",
    install_requires=[
        'pd_ecs @ git+https://github.com/HDictus/pd-ecs/',
        'pyglet',
        'behave'
    ],
    packages=find_packages(),
    python_requires=">=3.6",
    extras_require={"docs": ["sphinx", "sphinx-bluebrain-theme", "sphinxcontrib-bibtex"]},
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Education",
        "Intended Audience :: Science/Research",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Topic :: Scientific/Engineering :: Vision-Analyses",
    ],
)
