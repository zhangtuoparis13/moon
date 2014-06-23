from setuptools import setup, find_packages

setup(
    name='Moon',
    version='0.1.0',
    packages=find_packages(),
    author='DThom',
    author_email="thomas.duval@orange.com",
    url="http://www.github.com/waitwaitwait/moon",
    license='Apache License, Version 2.0',
    long_description=open('README.md').read(),
    test_suite="tests",
    package_dir={'moon': './'},
    install_requires=['django_openstack_auth', 'python-keystoneclient', 'python-novaclient'],
)
