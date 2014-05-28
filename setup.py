from setuptools import setup, find_packages

setup(
    name='Moon',
    version='0.1dev',
    packages=find_packages(),
    author='DThom',
    license='Apache License, Version 2.0',
    long_description=open('README.md').read(),
    test_suite="tests"
)
