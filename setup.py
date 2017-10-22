#!/usr/bin/env python

import os
from setuptools import setup
import sys


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name="asserts",
    version="0.7.1",
    description="Stand-alone Assertions",
    long_description=read("README.rst"),
    author="Sebastian Rittau",
    author_email="srittau@rittau.biz",
    url="https://github.com/srittau/python-asserts",
    py_modules=["asserts", "test_asserts"],
    data_files=[(
        "lib/python{}.{}/site-packages".format(*sys.version_info[:2]),
        ["asserts.pyi"],
    )],
    license="MIT",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Topic :: Software Development :: Quality Assurance",
        "Topic :: Software Development :: Testing",
    ],
)
