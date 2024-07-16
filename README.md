<h1 align="center">Confluence Space Management Toolkit</h1>
<p align="center">
    <a href="https://sonarqube.infrateam.xyz/dashboard?id=airslateinc_confluence-maintenance-tools">
        <img src="https://sonarqube.infrateam.xyz/api/project_badges/measure?project=airslateinc_confluence-maintenance-tools&metric=coverage&token=sqb_51b574060b2fa5e7fa6ac24f33e91fbbce7f2e73" alt="Coverage Status" />
    </a>
    <a href="https://sonarqube.infrateam.xyz/dashboard?id=airslateinc_confluence-maintenance-tools">
        <img src="https://sonarqube.infrateam.xyz/api/project_badges/measure?project=airslateinc_confluence-maintenance-tools&metric=alert_status&token=sqb_51b574060b2fa5e7fa6ac24f33e91fbbce7f2e73" alt="Quality Gate Status" />
    </a>
    <a href="https://sonarqube.infrateam.xyz/dashboard?id=airslateinc_confluence-maintenance-tools">
        <img src="https://sonarqube.infrateam.xyz/api/project_badges/measure?project=airslateinc_confluence-maintenance-tools&metric=security_rating&token=sqb_51b574060b2fa5e7fa6ac24f33e91fbbce7f2e73" alt="Security Rating" />
    </a>
    <a href="https://sonarqube.infrateam.xyz/dashboard?id=airslateinc_confluence-maintenance-tools">
        <img src="https://sonarqube.infrateam.xyz/api/project_badges/measure?project=airslateinc_confluence-maintenance-tools&metric=sqale_rating&token=sqb_51b574060b2fa5e7fa6ac24f33e91fbbce7f2e73" alt="Maintainability Rating" />
    </a>
</p>

Welcome to the Confluence Space Management Toolkit! This repository is 
designed to help you manage and maintain your Confluence spaces more 
efficiently. Currently, we have tools for exporting Confluence spaces, 
exporting page metadata, and exporting owner metadata, and we plan to add more 
useful features in the future.

## Tools

### Space Exporter

The Space Exporter script downloads all pages from a specified Confluence 
space and saves them locally in both HTML and JSON formats.

**Output structure:**

* The script saves HTML and JSON versions of each page in the `output/html` 
  and `output/json` directories, respectively.
* The directory structure mirrors the hierarchy of pages in Confluence.
* The `output` directory can be customized using the `--output-dir` option.

### Pages Metadata Exporter

The Pages Metadata Exporter script generates a CSV file with metadata about 
each page in a specified Confluence space, including whether the content is in 
English or contains Cyrillic characters, creation and last modification dates, 
owner, and more.

**Output structure:**

* The script saves `pages-metadata.csv` CSV file with metadata about each page 
  in the `output` directory.
* The `output` directory can be customized using the `--output-dir` option.

### Owner Metadata Exporter

The Owner Metadata Exporter script generates a CSV file with metadata about 
the owners of pages in a specified Confluence space, including information 
about whether the owner is unlicensed or deleted, the number of current and 
archived pages they own, the last contribution date, and a link to their 
profile.

**Output structure:**

* The script saves `owners-metadata.csv` CSV file with metadata about each 
  owner in the `output` directory.
* The `output` directory can be customized using the `--output-dir` option.

## Getting Started

### Prerequisites

What kind of things you need to install on your workstation to start:

* [Python](https://www.python.org/) >= 3.9
* [Git](https://git-scm.com/) >= 1.7.0

> [!NOTE]
> While this project might hypothetically work with Python 3.8 or earlier
> versions, I have not tested it on those versions. As such, I cannot guarantee
> its functionality on these older versions of Python. Given the age of these
> versions, if issues arise, I do not plan to address them.
>
> Though Python 3.9 is also somewhat outdated, I support it because it remains
> the default version on macOS. However, I do not recommend relying on continued
> support for Python 3.9. It is advisable to install a more recent version of
> Python, which is a straightforward process on both Linux and macOS.
>
> As for Windows users, with all the various issues and hacks they usually deal
> with, it’s safe to assume they already have the latest version of Python and
> likely work within WSL or maintain a native POSIX terminal environment.

### Installing

#### Recommended Installation Method

To use the Confluence Space Management Toolkit without modifying or exploring
its code, follow the steps below. This method is suitable for those who might be
new to Python and are unfamiliar with virtual environments.

##### Installation Using `pip`

The Confluence Space Management Toolkit is a Python package, and the recommended
installation method is using `pip`. This ensures that all dependencies are managed
correctly and the toolkit is isolated from other Python projects on your system.

###### Step-by-Step Guide

1. Ensure you have Python installed on your system (`python3 --version`).
2. Open a Terminal/Command Prompt
3. Run the following command to install the toolkit directly from GitHub.
   This will install the latest version of the toolkit.
   ```shell
    $ pip3 install --user --upgrade git+https://github.com/airslateinc/confluence-maintenance-tools.git#egg=confluence
   ```
4. After installation, you can verify that the toolkit is installed correctly
   by checking its version.
   ```shell
    $ confluence --version
   ```

###### Using Virtual Environment (Optional but Recommended)

Using a virtual environment is a good practice in Python as it creates an
isolated environment for your projects, avoiding conflicts with other Python
projects.

1. Run the following commands to create and activate a virtual environment.
   ```shell
    $ python3 -m venv .venv
    $ source .venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```
2. Once the virtual environment is activated, install the toolkit using pip.
   ```shell
    $ pip install --upgrade git+https://github.com/airslateinc/confluence-maintenance-tools.git#egg=confluence
    ```
3. Similar to the previous step, verify the installation.
   ```shell
    $ confluence --version
   ```

###### Installing Tagged Release

If you prefer to install a specific, stable version of the toolkit, you can use
a tagged release. Replace `v1.2.0` in the example below with the desired version:

```shell
# Without virtualenv
pip install --user --upgrade git+https://github.com/airslateinc/confluence-maintenance-tools.git@v1.2.0#egg=confluence

# Or, with virtualenv
pip install --upgrade git+https://github.com/airslateinc/confluence-maintenance-tools.git@v1.2.0#egg=confluence
````

###### Additional Resources

For more information on `pip` and Python packaging, visit the following links:

* [Install pip](https://pip.pypa.io/en/latest/installation/)
* [Python Packaging User Guide](https://packaging.python.org/)

#### Git way installation method (for developers)

To install Confluence Space Management Toolkits, follow these steps:

1. Clone the repository
2. Set up the project
3. Activate the virtual environment
4. Install project and all its dependencies
5. Create a `.env` file with your Confluence API credentials

###### Installation Steps

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

# Verify the installation
$ confluence --version
```

> [!IMPORTANT]
> The command `source .venv/bin/activate` activates the virtual
> environment. This step is not only part of the installation process but also
> mandatory for running the project when using the Git way installation method.
> Remember to activate the virtual environment once per terminal session.

More information about Python virtualenv can be found here:
[Python Virtualenv](https://docs.python.org/3/library/venv.html).

## Usage

### Creating the `.env` file

Before running the toolkit, you need to create a `.env` file in the root directory
with your Confluence API credentials. This file will store your API user and token
securely. Run the following commands to create the `.env` file and add your
Confluence API credentials:

```shell
# Create a .env file in the root directory and add the following variables:
$ echo "CONFLUENCE_API_USER=your-confluence-email" > .env
$ echo "CONFLUENCE_API_TOKEN=your-confluence-api-token" >> .env
```

You can create an API token in your Confluence account settings.
For more information, see [API Tokens](https://id.atlassian.com/manage-profile/security/api-tokens).

### Quick Start

```shell
$ confluence --help
```

### Exporting Confluence Space

To export all pages from a specified Confluence space:

```shell
$ confluence export --space-key YOUR_SPACE_KEY
```

### Exporting Page Metadata

To generate a CSV file with metadata about each page in a specified Confluence
space:

```shell
$ confluence pages-metadata --space-key YOUR_SPACE_KEY
```

### Exporting Owner Metadata

To generate a CSV file with metadata about the owners of pages in a specified
Confluence space:

```shell
$ confluence owners-metadata --space-key YOUR_SPACE_KEY
```

## Common Options

There are common options that can be used with all commands.

To specify the output directory:

```shell
$ confluence COMMAND --space-key YOUR_SPACE_KEY --output-dir YOUR_OUTPUT_DIR
```

If the `--output-dir` option is not specified, the `output` directory in the
current working directory will be used.

To suppress informational messages, use the `-q`, `--quiet` or `--silent`
option:

```shell
$ confluence -q <command> --space-key YOUR_SPACE_KEY
```

## Environment Variables

Our toolkit can obtain the necessary API credentials from the current
environment variables without reading from a `.env` file. This can be useful
for avoiding the storage of secrets in the project directory.

To run the scripts with environment variables directly, use the following
commands:

```shell
$ CONFLUENCE_API_USER=your-confluence-email \
> CONFLUENCE_API_TOKEN="your-confluence-api-token" \
> confluence export --space-key YOUR_SPACE_KEY

$ CONFLUENCE_API_USER=your-confluence-email \
> CONFLUENCE_API_TOKEN="your-confluence-api-token" \
> confluence pages-metadata --space-key YOUR_SPACE_KEY

$ CONFLUENCE_API_USER=your-confluence-email \
> CONFLUENCE_API_TOKEN="your-confluence-api-token" \
> confluence owners-metadata --space-key YOUR_SPACE_KEY
```

> [!WARNING]  
> Using environment variables directly in commands might expose
> your API credentials in the command history. Ensure to clear or manage your
> command history appropriately to avoid exposing sensitive information.

## Project Information

Confluence Space Management Toolkit is released under the
[MIT License](https://choosealicense.com/licenses/mit/), and its code lives at
[GitHub](https://github.com/airslateinc/confluence-maintenance-tools). It’s
rigorously tested on Python 3.9+.

If you'd like to contribute to Confluence Space Management Toolkit you're most
welcome!

## Support

Should you have any question, any remark, or if you find a bug, or if there is
something you can't do with the Confluence Space Management Toolkit, please
[open an issue](https://github.com/sergeyklay/confluence-maintenance-tools/issues).

## Credits

Confluence Space Management Toolkit is written and maintained by
[Serghei Iakovlev](https://github.com/sergeyklay/).

A full list of contributors can be found in
[GitHub's overview](https://github.com/airslateinc/confluence-maintenance-tools/graphs/contributors).
