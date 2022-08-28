#!/usr/bin/env python
# -*- coding: utf-8 -*-

import codecs
import os

from setuptools import setup


def read(fname):
    file_path = os.path.join(os.path.dirname(__file__), fname)
    return codecs.open(file_path, encoding="utf-8").read()


setup(
    name="inline",
    version="0.1.0",
    author="Yu Liu",
    author_email="yuki.liu@utexas.edu",
    maintainer="Yu Liu",
    maintainer_email="yuki.liu@utexas.edu",
    license="MIT",
    url="https://github.com/sweetStreet/pytest-inline",
    description="A simple plugin to use with pytest",
    long_description="TODO",  # read('README.rst'),
    packages=["inline"],
    python_requires=">=3.6",
    install_requires=["pytest>=7.0.0"],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Framework :: Pytest",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Testing",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: PyPy",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: MIT License",
    ],
    entry_points={
        "pytest11": [
            "inline = inline.conftest",
        ],
    },
    extras_require={
        "dev": ["flake8", "black", "pytest-html"],
    },
)
