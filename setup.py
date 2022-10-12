#!/usr/bin/env python3

'''Ejemplo de API REST para ADI'''

from setuptools import setup

setup(
    name='restlist',
    version='0.1',
    description=__doc__,
    packages=['restlist', 'restlist_scripts'],
    entry_points={
        'console_scripts': [
            'restlist_server=restlist_scripts.server:main',
            'restlist_client=restlist_scripts.client:main'
        ]
    }
)