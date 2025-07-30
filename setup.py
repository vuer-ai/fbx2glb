#!/usr/bin/env python
# -*- coding: utf-8 -*-

import io
import os
import sys
from setuptools import setup, find_packages

# Package meta-data
NAME = 'fbx2glb'
DESCRIPTION = 'Convert FBX files to GLB format for web-based 3D applications'
URL = 'https://github.com/fortyfive-ai/fbx2glb'
EMAIL = 'info@fortyfive.ai'
AUTHOR = 'FortyFive AI'
REQUIRES_PYTHON = '>=3.7.0'
VERSION = '0.1.0'

# What packages are required for this module to be executed?
REQUIRED = [
    'numpy>=1.20.0',
]

# What packages are optional?
EXTRAS = {
    'dev': [
        'pytest>=7.0.0',
        'black>=22.0.0',
        'isort>=5.10.0',
        'mypy>=0.940',
        'twine>=4.0.0',
    ],
}

# Import the README and use it as the long-description
here = os.path.abspath(os.path.dirname(__file__))

try:
    with io.open(os.path.join(here, 'README.md'), encoding='utf-8') as f:
        long_description = '\n' + f.read()
except FileNotFoundError:
    long_description = DESCRIPTION

# Load the package's __version__.py module as a dictionary
about = {}
if not VERSION:
    project_slug = NAME.lower().replace("-", "_").replace(" ", "_")
    with open(os.path.join(here, 'src', project_slug, '__version__.py')) as f:
        exec(f.read(), about)
else:
    about['__version__'] = VERSION

# Where the magic happens:
setup(
    name=NAME,
    version=about['__version__'],
    description=DESCRIPTION,
    long_description=long_description,
    long_description_content_type='text/markdown',
    author=AUTHOR,
    author_email=EMAIL,
    python_requires=REQUIRES_PYTHON,
    url=URL,
    packages=find_packages(exclude=["tests", "*.tests", "*.tests.*", "tests.*"]),
    entry_points={
        'console_scripts': [
            'fbx2glb=fbx2glb.cli:main',
            'fbx2glb-batch=fbx2glb.batch:main',
            'fbx2glb-component=fbx2glb.component:main',
        ],
    },
    install_requires=REQUIRED,
    extras_require=EXTRAS,
    include_package_data=True,
    license='MIT',
    classifiers=[
        # Trove classifiers
        # Full list: https://pypi.python.org/pypi?%3Aaction=list_classifiers
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: Implementation :: CPython',
        'Topic :: Multimedia :: Graphics :: 3D Modeling',
        'Topic :: Multimedia :: Graphics :: 3D Conversion',
    ],
)
