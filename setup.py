"""
Install with `pip install .`
"""
from setuptools import setup, find_packages
from setuptools.command.test import test as TestCommand
import codecs
import io
import re
import os

import parserbot

here = os.path.abspath(os.path.dirname(__file__))

def read(*parts):
    # intentionally *not* adding an encoding option to open
    return codecs.open(os.path.join(here, *parts), 'r').read()

def find_version(*file_paths):
    version_file = read(*file_paths)
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]",
                              version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")

long_description = read('README.md')

class PyTest(TestCommand):
    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = ['--strict', '--verbose', '--tb=long', 'tests']
        self.test_suite = True

    def run_tests(self):
        import pytest
        errno = pytest.main(self.test_args)
        sys.exit(errno)

setup(
    name='parserbot',
    version=find_version('parserbot', '__init__.py'),
    url='http://github.com/mailbackwards/parserbot/',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'Flask>=0.10.1',
        'nltk>=3.0.1',
        'requests>=2.5.1'
    ],
    cmdclass={'test': PyTest},
    #license='LGPL' # TODO: decide on license
    author='MIT HyperStudio',
    author_email='hyperstudio@mit.edu',
    test_suite='test',
    tests_require=['pytest'],
    extras_require={
        'testing': ['pytest'],
    },
    description='Natural Language services and APIs all in one place',
    long_description=long_description
)