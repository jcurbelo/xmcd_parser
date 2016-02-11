from setuptools import setup, find_packages
from os import path

here = path.abspath(path.dirname(__file__))

setup(
    name='xmcd_parser',

    version='0.0.1',

    license='MIT',

    packages=find_packages(exclude=['contrib', 'docs', 'tests']),
)