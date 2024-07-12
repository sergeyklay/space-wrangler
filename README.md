# Confluence Maintenance Tools

Welcome to the Confluence Maintenance Tools project! This repository is designed
to help you manage and maintain your Confluence spaces more efficiently. Currently,
we have a Space Exporter tool, and we plan to add more useful features in the future.

## Space Exporter

The Space Exporter script downloads all pages from a specified Confluence space
and saves them locally in both HTML and JSON formats. Additionally, it generates
a CSV file with detailed information about each page, including whether the content
is in English or contains Cyrillic characters.

### Features

- Downloads all pages from a specified Confluence space.
- Saves pages as HTML and JSON files in a structured directory format.
- Generates a CSV file with metadata about each page, including:
  - Page ID
  - Page Title
  - Created Date
  - Last Updated Date
  - Last Editor
  - Current Owner
  - Page URL
  - Content Language (English or contains Cyrillic)

### Output Structure

- HTML and JSON Files:
  - The script saves HTML and JSON versions of each page in the `output/html`
    and `output/json` directories, respectively.
  - The directory structure mirrors the hierarchy of pages in Confluence.
- CSV File:
  - `output/all_pages.csv` contains metadata about each page
  - Columns include:
    - Page ID
    - Page Title
    - Created Date
    - Last Updated Date
    - Last Editor
    - Current Owner
    - Page URL
    - Content Language (English or contains Cyrillic)

## Installation

###  Requirements

- Python 3.10+

### Installing the Confluence Maintenance Tools

Confluence Maintenance Tools is a Python-only package and the recommended
installation method is installing into a virtualenv. The master of all the material
is the Git repository at https://github.com/airslateinc/confluence-maintenance-tools.
So, can also install the latest unreleased development version directly from the
`main` branch on GitHub. It is a work-in-progress of a future stable release so
the experience might be not as smooth.:

```shell
# Without virtualenv
$ pip install --user --upgrade git+ssh://git@github.com/airslateinc/confluence-maintenance-tools.git#egg=confluence

# Or, with virtualenv
$ pip install --upgrade git+ssh://git@github.com/airslateinc/confluence-maintenance-tools.git#egg=confluence
```

This command will download the latest version of `confluence` from the Git repo and install it to your system.

Note: The main branch will always contain the latest unstable version, so the experience might be not as smooth.

Verify that now we have the current development version identifier, for example:

```shell
$ confluence --version
confluence 1.0.0
Copyright (C) 2024 airSlate, Inc..
This is free software; see the source for copying conditions. There is NO
warranty; not even for MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
```

To install tagged release use command as follows (replace v1.0.0 in example bellow):

```shell
# Without virtualenv
$ pip install --user --upgrade git+ssh://git@github.com/airslateinc/confluence-maintenance-tools.git@v1.0.0#egg=confluence

# Or, with virtualenv
$ pip install --upgrade git+ssh://git@github.com/airslateinc/confluence-maintenance-tools.git@v1.0.0#egg=confluence
```

Finally, create a `.env` file in the root directory of the project and add the following variables:
  ```shell
  CONFLUENCE_API_USER=your-confluence-email
  CONFLUENCE_API_TOKEN=your-confluence-api-token
  CONFLUENCE_SPACE_KEY=your-space-key
  ```

More information about pip and PyPI can be found here:

- [Install pip](https://pip.pypa.io/en/latest/installation/)
- [Python Packaging User Guide](https://packaging.python.org/)

#### Installing Git version (not recommended)

There is a way to use `confluence` CLI tool without pip.

1. Clone the repository
2. Go to project root
3. Run `python -m pip install --user -r requirements.txt`
4. To call `confluence` use `python -m confluence`

## Usage

### Command Line Options

#### Quick Start

```shell
confluence --help
```

#### Synopsis:

```shell
confluence [options]
```
