from setuptools import setup
import os


version = '0.1'

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.rst')).read()
HISTORY = open(os.path.join(here, 'HISTORY.rst')).read()


setup(
    name='buildout.variables',
    version=version,
    description="Adds small features to zc.recipe.cmmi",
    long_description=README + "\n\n" + HISTORY,
    author='Florian Schulze',
    author_email='florian.schulze@gmx.net',
    url='http://github.com/fschulze/buildout.variables',
    include_package_data=True,
    packages=['buildout', 'buildout.variables'],
    namespace_packages=['buildout'],
    install_requires=[
        'RSFile'],
    entry_points={
        'zc.buildout':
            ['default = buildout.variables:Recipe']})
