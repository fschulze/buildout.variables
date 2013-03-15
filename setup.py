from setuptools import setup
from setuptools.command.test import test as TestCommand
import os

version = '0.3'

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.rst')).read()
HISTORY = open(os.path.join(here, 'HISTORY.rst')).read()


class PyTest(TestCommand):
    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        #import here, cause outside the eggs aren't loaded
        import pytest
        import sys
        errno = pytest.main(self.test_args)
        sys.exit(errno)


setup(
    name='buildout.variables',
    version=version,
    description="Provides dynamic variables in buildouts",
    long_description=README + "\n\n" + HISTORY,
    author='Florian Schulze',
    author_email='florian.schulze@gmx.net',
    url='http://github.com/fschulze/buildout.variables',
    license='GPL',
    include_package_data=True,
    packages=['buildout', 'buildout.variables'],
    namespace_packages=['buildout'],
    cmdclass=dict(test=PyTest),
    tests_require=[
        'pytest',
        'pytest-cov'],
    install_requires=[
        'RSFile'],
    entry_points={
        'zc.buildout':
            ['default = buildout.variables:Recipe']})
