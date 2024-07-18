# This file is part of the confluence.
#
# Copyright (c) 2024 airSlate, Inc.
#
# For the full copyright and license information, please view
# the LICENSE file that was distributed with this source code.

"""Setup module for confluence.

This module contains the setup configuration for the confluence package.
"""

import codecs
import re
from os import path

from setuptools import find_packages, setup


def read_file(filepath):
    """Read content from a UTF-8 encoded text file.

    Args:
        filepath (str): Path to the file.

    Returns:
        str: Content of the file.
    """
    with codecs.open(filepath, 'rb', 'utf-8') as file_handle:
        return file_handle.read()


PKG_NAME = 'confluence'
PKG_DIR = path.abspath(path.dirname(__file__))
META_PATH = path.join(PKG_DIR, PKG_NAME, '__init__.py')
META_CONTENTS = read_file(META_PATH)

# Version regex according to PEP 440
VERSION_REGEX = (r'([1-9][0-9]*!)?(0|[1-9][0-9]*)(\.(0|[1-9][0-9]*))'
                 r'*((a|b|rc)(0|[1-9][0-9]*))?(\.post(0|[1-9][0-9]*))'
                 r'?(\.dev(0|[1-9][0-9]*))?')


def is_canonical_version(version):
    """Check if a version string is in the canonical format of PEP 440.

    Args:
        version (str): Version string to check.

    Returns:
        bool: True if the version string is in canonical format, False
            otherwise.
    """
    pattern = fr'^{VERSION_REGEX}$'
    return re.match(pattern, version) is not None


def find_meta(meta):
    """Extract __*meta*__ from META_CONTENTS.

    Args:
        meta (str): Metadata key to find.

    Returns:
        str: Value of the metadata key.

    Raises:
        RuntimeError: If the metadata key is not found.
    """
    meta_match = re.search(
        r"^__{meta}__\s+=\s+['\"]([^'\"]*)['\"]".format(meta=meta),
        META_CONTENTS,
        re.M
    )

    if meta_match:
        return meta_match.group(1)
    raise RuntimeError(
        f'Unable to find __{meta}__ string in package meta file')


def get_version_string():
    """Return package version as listed in `__version__` in meta file.

    Returns:
        str: Package version string.

    Raises:
        ValueError: If the detected version string is not in canonical format.
    """
    # Parse version string
    version_string = find_meta('version')

    # Check validity
    if not is_canonical_version(version_string):
        message = (
            'The detected version string "{}" is not in canonical '
            'format as defined in PEP 440.'.format(version_string))
        raise ValueError(message)

    return version_string


# What does this project relate to.
KEYWORDS = [
    'confluence',
    'cli',
    'maintenance',
]

# Classifiers: available ones listed at https://pypi.org/classifiers
CLASSIFIERS = [
    'Development Status :: 5 - Production/Stable',

    'Environment :: Console',

    'Intended Audience :: Developers',
    'Intended Audience :: System Administrators',
    'Intended Audience :: Information Technology',

    'Natural Language :: English',

    'License :: OSI Approved :: MIT',
    'Operating System :: OS Independent',

    'Programming Language :: Python',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.9',
    'Programming Language :: Python :: 3.10',
    'Programming Language :: Python :: 3.11',
    'Programming Language :: Python :: 3.12',
    'Programming Language :: Python :: 3.13',
    'Programming Language :: Python :: 3.14',
    'Programming Language :: Python :: 3 :: Only',

    'Topic :: System :: Software Distribution',
    'Topic :: Software Development :: Build Tools',
]

# Dependencies that are downloaded by pip on installation and why.
INSTALL_REQUIRES = [
    'atlassian-python-api>=3.41.0',  # Python wrapper for Atlassian REST APIs.
    'beautifulsoup4>=4.12.0',  # HTML and XML parser.
    'click>=8.1.0',  # Composable command line interface toolkit.
    'python-dotenv>=1.0.1',  # Get values from your environment files.
    'requests>=2.32.0',  # Python HTTP for Humans.
    'types-requests>=2.32.0',  # Type hints for requests.
]

# Project's URLs
PROJECT_URLS = {
    'Bug Tracker': 'https://github.com/airslateinc/confluence-maintenance-tools/issues',  # noqa: E501
    'Changelog': f"{find_meta('url')}/releases",
    'Documentation': f"{find_meta('url')}?tab=readme-ov-file",
    'Source Code': find_meta('url'),
}

DEPENDENCY_LINKS = []

# List additional groups of dependencies here (e.g. testing dependencies).
# You can install these using the following syntax, for example:
#
#    $ pip install -e .[testing,docs,develop]
#
EXTRAS_REQUIRE = {
    'testing': [
        'check-manifest>=0.45',  # Check MANIFEST.in file
        'coverage[toml]>=6.0',  # Code coverage measurement for Python
        'flake8-blind-except>=0.2.0',  # Checks for blind except: statements
        'flake8-import-order>=0.18.1',  # Checks the ordering of imports
        'flake8>=6.0.0',  # The modular source code checker
        'mypy>=1.100.0',  # Optional static type checker
        'pylint>=2.6.2',  # Python code static checker
        'pytest-mock>=3.14.0',  # Thin-wrapper around the mock package for easier use with py.test  # noqa: E501
        'pytest>=8.0.0',  # Our tests framework
    ],
    'docs': [],
}

# Dependencies that are required to develop package
DEVELOP_REQUIRE = [
    'build>=1.2.0',  # A simple, correct Python build frontend
]

EXTRAS_REQUIRE['develop'] = \
    DEVELOP_REQUIRE + EXTRAS_REQUIRE['testing'] + EXTRAS_REQUIRE['docs']

ENTRY_POINTS = {
    'console_scripts': [
        f'{PKG_NAME}={PKG_NAME}.cli:main'
    ]
}

if __name__ == '__main__':
    setup(
        name=PKG_NAME,
        version=get_version_string(),
        author=find_meta('author'),
        author_email=find_meta('author_email'),
        maintainer=find_meta('author'),
        maintainer_email=find_meta('author_email'),
        license=find_meta('license'),
        description=find_meta('description'),
        long_description=find_meta('description'),
        long_description_content_type='text/markdown',
        keywords=KEYWORDS,
        url=find_meta('url'),
        project_urls=PROJECT_URLS,
        classifiers=CLASSIFIERS,
        packages=find_packages(exclude=['tests.*', 'tests']),
        platforms='any',
        include_package_data=True,
        zip_safe=False,
        python_requires='>=3.9, <4',
        install_requires=INSTALL_REQUIRES,
        dependency_links=DEPENDENCY_LINKS,
        extras_require=EXTRAS_REQUIRE,
        entry_points=ENTRY_POINTS,
    )
