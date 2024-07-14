# Confluence Space Management Toolkit

[![Coverage](https://sonarqube.infrateam.xyz/api/project_badges/measure?project=airslateinc_confluence-maintenance-tools&metric=coverage&token=sqb_51b574060b2fa5e7fa6ac24f33e91fbbce7f2e73)](https://sonarqube.infrateam.xyz/dashboard?id=airslateinc_confluence-maintenance-tools)
[![Quality Gate Status](https://sonarqube.infrateam.xyz/api/project_badges/measure?project=airslateinc_confluence-maintenance-tools&metric=alert_status&token=sqb_51b574060b2fa5e7fa6ac24f33e91fbbce7f2e73)](https://sonarqube.infrateam.xyz/dashboard?id=airslateinc_confluence-maintenance-tools)
[![Security Rating](https://sonarqube.infrateam.xyz/api/project_badges/measure?project=airslateinc_confluence-maintenance-tools&metric=security_rating&token=sqb_51b574060b2fa5e7fa6ac24f33e91fbbce7f2e73)](https://sonarqube.infrateam.xyz/dashboard?id=airslateinc_confluence-maintenance-tools)
[![Maintainability Rating](https://sonarqube.infrateam.xyz/api/project_badges/measure?project=airslateinc_confluence-maintenance-tools&metric=sqale_rating&token=sqb_51b574060b2fa5e7fa6ac24f33e91fbbce7f2e73)](https://sonarqube.infrateam.xyz/dashboard?id=airslateinc_confluence-maintenance-tools)

Welcome to the Confluence Space Management Toolkit! This repository is designed
to help you manage and maintain your Confluence spaces more efficiently. Currently,
we have tools for exporting Confluence spaces and exporting page metadata, and
we plan to add more useful features in the future.

## Tools

### Space Exporter

The Space Exporter script downloads all pages from a specified Confluence space
and saves them locally in both HTML and JSON formats.

**Output structure:**

- The script saves HTML and JSON versions of each page in the `output/html`
  and `output/json` directories, respectively.
- The directory structure mirrors the hierarchy of pages in Confluence.
- The `output` directory can be customized using the `--output-dir` option.

### Metadata Exporter

The Metadata Exporter script generates a CSV file with metadata about each page
in a specified Confluence space, including whether the content is in English or
contains Cyrillic characters, creation and last modification dates, owner, and
more.

**Output structure:**

- The script saves `pages-metadata.csv` CSV file with metadata about each page
  in the `output` directory.
- The `output` directory can be customized using the `--output-dir` option.

## Installation

###  Requirements

- Python 3.10+

### Installing the Confluence Space Management Toolkits

To install Confluence Space Management Toolkits, follow these steps:

1. Clone the repository
2. Set up the project
3. Activate the virtual environment
4. Install project and all its dependencies
5. Create a `.env` file with your Confluence API credentials

#### Steps:

```shell
# Clone the repository
$ git clone git@github.com:airslateinc/confluence-maintenance-tools.git
$ cd confluence-maintenance-tools

# Set project up
$ make init

# Activate the virtual environment
$ source .venv/bin/activate  # On Windows use `venv\Scripts\activate`

# Install project and all its dependencies
$ make install

# Create a .env file in the root directory and add the following variables:
$ echo "CONFLUENCE_API_USER=your-confluence-email" > .env
$ echo "CONFLUENCE_API_TOKEN=your-confluence-api-token" >> .env
```

> [!IMPORTANT]
> The command `source .venv/bin/activate` activates the virtual
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
$ confluence --help
```

### Exporting Confluence Space

To export all pages from a specified Confluence space:

```shell
$ confluence export --space-key YOUR_SPACE_KEY
```

To specify the output directory:

```shell
$ confluence export --space-key YOUR_SPACE_KEY --output-dir /path/to/directory
```

If the `--output-dir` option is not specified, the `./output` directory in the
current working directory will be used.

### Exporting Page Metadata

To export metadata of all pages from a specified Confluence space:

```shell
$ confluence pages-metadata --space-key YOUR_SPACE_KEY
```

To specify the output directory:

```shell
$ confluence pages-metadata --space-key YOUR_SPACE_KEY --output-dir /path/to/directory
```

If the `--output-dir` option is not specified, the `./output` directory in the
current working directory will be used.

## Maintainers

- [Serghei Iakovlev](https://github.com/sergeyklay)
