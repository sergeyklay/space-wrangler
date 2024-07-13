# Confluence Space Management Toolkit

Welcome to the Confluence Space Management Toolkit! This repository is designed
to help you manage and maintain your Confluence spaces more efficiently. Currently,
we have tools for exporting Confluence spaces and exporting page metadata, and
we plan to add more useful features in the future.

## Tools

### Space Exporter

The Space Exporter script downloads all pages from a specified Confluence space
and saves them locally in both HTML and JSON formats.

#### Output Structure

- The script saves HTML and JSON versions of each page in the `output/html`
  and `output/json` directories, respectively.
- The directory structure mirrors the hierarchy of pages in Confluence.
- The `output` directory can be customized using the `--output-dir` option.

### Metadata Exporter

The Metadata Exporter script generates a CSV file with metadata about each page
in a specified Confluence space, including whether the content is in English or
contains Cyrillic characters, creation and last modification dates, owner, and more.

#### Output Structure

- The script saves `pages-metadata.csv` CSV file with metadata about each page
  in the `output` directory.
- The `output` directory can be customized using the `--output-dir` option.

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
$ python3 -m venv venv
$ source venv/bin/activate  # On Windows use `venv\Scripts\activate`

# Install dependencies
$ pip install -r requirements.txt

# Create a .env file in the root directory and add the following variables:
$ echo "CONFLUENCE_API_USER=your-confluence-email" > .env
$ echo "CONFLUENCE_API_TOKEN=your-confluence-api-token" >> .env
```

> [!NOTE]
> Using `python3 -m venv venv` instead of `python -m venv venv` ensures
> that you're explicitly using Python 3, which is necessary for compatibility
> with this project.


> [!IMPORTANT]
> The command `source venv/bin/activate` activates the virtual
> environment. This step is not only part of the installation
> process but also mandatory for running the project. Remember
> to activate the virtual environment once per terminal session.

You can create an API token in your Confluence account settings. For more
information,  see https://id.atlassian.com/manage-profile/security/api-tokens

More information about Python virtualenv can be found here:
https://docs.python.org/3/library/venv.html

## Usage

### Quick Start

```shell
$ python -m confluence --help
```

### Exporting Confluence Space

To export all pages from a specified Confluence space:

```shell
$ python -m confluence export --space-key YOUR_SPACE_KEY
```

To specify the output directory:

```shell
$ python -m confluence export --space-key YOUR_SPACE_KEY --output-dir /path/to/directory
```

If the `--output-dir` option is not specified, the `./output` directory in the
current working directory will be used.

### Exporting Page Metadata

To export metadata of all pages from a specified Confluence space:

```shell
$ python -m confluence metadata --space-key YOUR_SPACE_KEY
```

To specify the output directory:

```shell
$ python -m confluence metadata --space-key YOUR_SPACE_KEY --output-dir /path/to/directory
```

If the `--output-dir` option is not specified, the `./output` directory in the
current working directory will be used.
