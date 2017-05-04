#!/usr/bin/env python

from setuptools import setup

setup(
    name='scox',
    version='1.0',
    description='NPC generator for INS-MV 4',
    author='Bertrand Moreau',
    author_email='moreau.bertrand@gmail.com',
    url='https://github.com/bmoreau/scox-gen',
    license='BSD 3-Clause',
    py_modules=['scx'],
    packages=['scox'],
    package_data={'scox': ['profiles/demons/*.scx',
                           'profiles/angels/*.scx',
                           'profiles/archetypes/*.scx']},
    install_requires=['Click'],
    entry_points='''
            [console_scripts]
            scx=scx:scx
        ''',
)
