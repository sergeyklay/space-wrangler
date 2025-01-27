# Space Wrangler

Welcome to the Space Wrangler! This toolkit is designed to help you efficiently
manage and maintain your Confluence spaces. Currently, it includes tools for
exporting spaces its metadata, with more features planned.

## Tools

### Space Exporter

Export all pages from a specified Confluence space in HTML, JSON, and plain text
formats.

**Output structure:**

* Saves files in `output/<SPACE-KEY>/html` `output/<SPACE-KEY>/json`,
  and `output/<SPACE-KEY>/txt` directories.
* Directory structure mirrors the hierarchy of Confluence pages.
* Customize the output directory with the `--output-dir` option.

### Space Metadata Exporter

Generate a CSV file with metadata about each space in your Confluence.

**Output structure:**

* CSV file `all-spaces.csv` saved in the `output/` directory.
* Customize the `output` directory with the `--output-dir` option.

### Pages Metadata Exporter

Generate a CSV file with metadata about each page in specified Confluence spaces.

**Output structure:**

* CSV file `pages-metadata.csv` saved in the `output/<SPACE-KEY>/csv` directory.
* Customize the `output` directory with the `--output-dir` option.

### Owner Metadata Exporter

Generate a CSV file with metadata about the owners of pages in specified
Confluence spaces.

**Output structure:**

* CSV file `owners-metadata.csv` saved in the `output/<SPACE-KEY>/csv` directory.
* Customize the output directory with the `--output-dir` option.

## Getting Started

### Prerequisites

What kind of things you need to install on your workstation to start:

* [Python](https://www.python.org/) >= 3.10
* [Git](https://git-scm.com/) >= 1.7.0
* [Poetry](https://python-poetry.org/) >= 1.8.1

> [!NOTE]
> While this toolkit might hypothetically work with Python 3.9 or earlier
> versions, I have not tested it on those versions. As such, I cannot guarantee
> its functionality on these older versions of Python. Given the age of these
> versions, if issues arise, I do not plan to address them.

### Installing

To install Confluence Space Management Toolkits, follow these steps:

1. Clone the repository
2. Set up the project
3. Activate the virtual environment
4. Install toolkit and all its dependencies
5. Verify the installation

#### Installation Steps

1. Clone the repository:
   ```shell
   git clone git@github.com:sergeyklay/space-wrangler.git
   cd space-wrangler
   ```
2. Set up virtual environment:
   ```shell
   python -m venv .venv
   ```
3. Activate the virtual environment:
   ```shell
   source .venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```
4. Install the toolkit and dependencies:
   ```shell
   poetry install
   ```
5. Verify the installation:
   ```shell
   swrangler --version
   ```

> [!IMPORTANT]
> The command `source .venv/bin/activate` activates the virtual
> environment. This step is not only part of the installation process but also
> mandatory for running the toolkit when using the Git way installation method.
> Remember to activate the virtual environment once per terminal session.

More information about Python virtualenv can be found here:
[Python Virtualenv](https://docs.python.org/3/library/venv.html).

## Usage

Before using the toolkit, provide your Confluence API credentials.

### Environment Variables

Set the following environment variables:

- `CONFLUENCE_API_USER`: Your Confluence email address.
- `CONFLUENCE_API_TOKEN`: Your Confluence API token.
- `CONFLUENCE_DOMAIN`: Your Confluence domain.

You can obtain an API token from
[Confluence API Tokens section](https://id.atlassian.com/manage-profile/security/api-tokens).
You cannot use your regular password for the API token.

### Creating the `.confluence` File

Create a `.confluenc`e file with your credentials in the current working
directory or home directory:

```shell
echo CONFLUENCE_API_USER="your-confluence-email" > .confluence
echo CONFLUENCE_API_TOKEN="your-confluence-api-token" >> .confluence
echo CONFLUENCE_DOMAIN="your-confluence-domain" >> .confluence
```

### Quick Start

```shell
swrangler --help
```

### Exporting Confluence Space

To export all pages from specified Confluence spaces:

```shell
swrangler export-space --space-key SPACE_KEY1,SPACE_KEY2
```

### Exporting Spaces Metadata

To generate a CSV file with metadata about all Confluence spaces:

```shell
swrangler spaces-metadata
```

### Exporting Page Metadata

To generate a CSV file with metadata about each page in specified Confluence
spaces:

```shell
swrangler pages-metadata --space-key SPACE_KEY1,SPACE_KEY2
```

### Exporting Owner Metadata

To generate a CSV file with metadata about the owners of pages in specified
Confluence spaces:

```shell
swrangler owners-metadata --space-key SPACE_KEY1,SPACE_KEY2
```

## Common Options

There are common options that can be used with all commands.

To specify the output directory:

```shell
swrangler COMMAND --space-key SPACE_KEY --output-dir OUTPUT_DIR
```

If the `--output-dir` option is not specified, the `output` directory in the
current working directory will be used.

To suppress informational messages, use the `-q`, `--quiet` or `--silent`
option:

```shell
swrangler -q <command> --space-key SPACE_KEY
```

## Support

Should you have any question, any remark, or if you find a bug, or if there is
something you can't do with the Space Wrangler, please
[open an issue](https://github.com/sergeyklay/space-wrangler/issues).

## Credits

Space Wrangler is written and maintained by
[Serghei Iakovlev](https://github.com/sergeyklay/). Contributors are listed on
[GitHub's overview](https://github.com/sergeyklay/space-wrangler/graphs/contributors).

## License

Space Wrangler is free software licensed under the
[GNU General Public Licence version 3]([LICENSE](https://choosealicense.com/licenses/gpl-3.0/)).
Copyright © 2024 Serghei Iakovlev.

### Note On Copyright Years

In copyright notices where the copyright holder is Serghei Iakovlev, then where
a range of years appears, this is an inclusive range that applies to every year
in the range.  For example: 2023-2025 represents the years 2023, 2024 and 2025.
