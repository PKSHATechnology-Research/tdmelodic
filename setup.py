#!/usr/bin/env python

from setuptools import setup, find_packages
from os import path
import re, io

def _readme():
    with open('README.md') as readme_file:
        return readme_file.read().replace(":copyright:", "(c)")

def _requirements():
    root_dir = path.abspath(path.dirname(__file__))
    return [name.rstrip() for name in open(path.join(root_dir, 'requirements.txt')).readlines()]

def _get_version():
    version = re.search(
        r'__version__\s*=\s*[\'"]([^\'"]*)[\'"]',  # It excludes inline comment too
        io.open('tdmelodic/__init__.py', encoding='utf_8_sig').read()
        ).group(1)
    return version

setup(
    name="tdmelodic",
    author="Hideyuki Tachibana",
    author_email='h_tachibana@pkshatech.com',
    python_requires='>=3.7',

    description="tdmelodic: Tokyo Japanese Accent Estimator",
    long_description=_readme(),

    install_requires=_requirements(),
    tests_requires=_requirements(),
    setup_requires=[],

    include_package_data=True,
    packages=find_packages(include=['tdmelodic', 'tdmelodic.*']),

    version=_get_version(),
    zip_safe=False,
)
