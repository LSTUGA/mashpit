#!/usr/bin/env python3

from setuptools import setup

setup(
    name='mashpit',
    version='0.7.3',
    url='https://github.com/tongzhouxu/mashpit',
    author='Tongzhou Xu',
    author_email='tongzhou.xu@uga.edu',
    description='A sketch-based surveillance platform',
    packages=['scripts'],
    scripts=[
        'scripts/create_db.py',
        'scripts/metadata_sra_db.py',
        'scripts/query_against_db.py',
        'scripts/sketch_db.py',
    ],
    install_requires=[
        'cython~=0.29.21',
        'screed~=1.0.4',
        'sourmash~=3.3.1',
        'pandas~=1.0.5',
        'setuptools~=47.1.1',
        'biopython~=1.78',
        'scipy~=1.5.4'
    ],
)
