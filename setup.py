# -*- coding: utf-8 -*-

# Learn more: https://github.com/kennethreitz/setup.py

from setuptools import setup, find_packages


with open('README.rst') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='CommandCoin',
    version='0.0.1',
    description='Personal finance tracker',
    long_description=readme,
    author='Starlinetor',
    author_email='eaccontent@gmail.com',
    url='https://github.com/starlinetor/CommandCoin',
    license=license,
    packages=find_packages(exclude=('tests', 'docs'))
)

