#  Created by Martin Strohalm

from setuptools import setup, find_packages

# get version
from pero import version
version = '.'.join(str(x) for x in version)

# get description
with open("README.md", "r") as fh:
    long_description = fh.read()

# include additional files
package_data = {}

# set classifiers
classifiers = [
    'Development Status :: 3 - Alpha',
    'Programming Language :: Python :: 3 :: Only',
    'Operating System :: OS Independent',
    'Topic :: Multimedia :: Graphics :: Presentation',
    'Topic :: Scientific/Engineering',
    'Intended Audience :: Developers',
    'Intended Audience :: Science/Research']

# main setup
setup(
    name = 'pero',
    version = version,
    description = 'Draw consistently with various backends',
    long_description = long_description,
    long_description_content_type='text/markdown',
    url = 'https://github.com/xxao/pero',
    author = 'Martin Strohalm',
    author_email = 'pero@bymartin.cz',
    license = 'MIT',
    packages = find_packages(),
    package_data = package_data,
    classifiers = classifiers,
    install_requires = ['numpy', 'Pillow'],
    zip_safe = False)
