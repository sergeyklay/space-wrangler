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
- Generates a CSV file with metadata about each page.

### Output Structure

- HTML and JSON Files:
  - The script saves HTML and JSON versions of each page in the `output/html`
    and `output/json` directories, respectively.
  - The directory structure mirrors the hierarchy of pages in Confluence.
- CSV File:
  - `output/all_pages.csv` contains metadata about each page

## Installation

###  Requirements

- Python 3.10+

### Installing the Confluence Maintenance Tools

We highly recommend using `virtualenv` for installing and running the Confluence
Maintenance Tools to avoid dependency conflicts. Follow these steps:

1. Clone the repository
2. Create and activate a virtual environment
3. Install the required dependencies
4. Create a `.env` file with your Confluence API credentials

#### Steps:

```shell
# Clone the repository
$ git clone git@github.com:airslateinc/confluence-maintenance-tools.git
$ cd confluence-maintenance-tools

# Create and activate virtual environment
$ python -m venv venv
$ source venv/bin/activate  # On Windows use `venv\Scripts\activate`

# Install dependencies
$ pip install -r requirements.txt

# Create a .env file in the root directory and add the following variables:
$ echo "CONFLUENCE_API_USER=your-confluence-email" > .env
$ echo "CONFLUENCE_API_TOKEN=your-confluence-api-token" >> .env
```

More information about pip and PyPI can be found here:

- [venv — Creation of virtual environments](https://docs.python.org/3/library/venv.html)

## Usage

### Command Line Options

#### Quick Start

```shell
$ python -m confluence --help
```

#### Synopsis

```shell
$ confluence [options]
```

#### Exporting Confluence Space

To export all pages from a specified Confluence space:

```shell
$ python -m confluence --export --space-key YOUR_SPACE_KEY
```

To specify the output directory:

```shell
$ python -m confluence --export --space-key YOUR_SPACE_KEY --output-dir /path/to/directory
```

If the --output-dir option is not specified, the `./output` directory in the
current working directory will be used.
