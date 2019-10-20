#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function
if False:
    from typing import Any, Dict, Generator, List, Tuple

import os
import sys

import itertools

def version():
    # type: () -> str
    version_py = os.path.join(os.path.dirname(__file__), "zulip", "__init__.py")
    with open(version_py) as in_handle:
        version_line = next(itertools.dropwhile(lambda x: not x.startswith("__version__"),
                                                in_handle))
    version = version_line.split('=')[-1].strip().replace('"', '')
    return version

def recur_expand(target_root, dir):
    # type: (Any, Any) -> Generator[Tuple[str, List[str]], None, None]
    for root, _, files in os.walk(dir):
        paths = [os.path.join(root, f) for f in files]
        if len(paths):
            yield os.path.join(target_root, root), paths

# We should be installable with either setuptools or distutils.
package_info = dict(
    name='zulip',
    version=version(),
    description='Bindings for the Zulip message API',
    author='Zulip Open Source Project',
    author_email='zulip-devel@googlegroups.com',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Topic :: Communications :: Chat',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    python_requires='>=2.7,!=3.0.x,!=3.1.x,!=3.2.x,!=3.3.x,!=3.4.x',
    url='https://www.zulip.org/',
    data_files=list(recur_expand('share/zulip', 'integrations')),
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'zulip-send=zulip.send:main',
            'zulip-api-examples=zulip.api_examples:main',
            'zulip-matrix-bridge=integrations.bridge_with_matrix.matrix_bridge:main',
        ],
    },
    package_data={'zulip': ["py.typed"]},
)  # type: Dict[str, Any]

setuptools_info = dict(
    install_requires=['requests[security]>=0.12.1',
                      'six',
                      'typing>=3.5.2.2;python_version<"3.5"',
                      'matrix_client',
                      ],
)

try:
    from setuptools import setup, find_packages
    package_info.update(setuptools_info)
    package_info['packages'] = find_packages(exclude=['tests'])

except ImportError:
    from distutils.core import setup
    from distutils.version import LooseVersion
    # Manual dependency check
    try:
        import requests
        assert(LooseVersion(requests.__version__) >= LooseVersion('0.12.1'))
    except (ImportError, AssertionError):
        print("requests >=0.12.1 is not installed", file=sys.stderr)
        sys.exit(1)

    package_info['packages'] = ['zulip']


setup(**package_info)
