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

### How to Use

1. Clone the repository
2. Install dependencies:
  ```shell
  $ pip install -r requirements.txt
  ```
3. Set up environment variables:
  Create a .env file in the root directory of the project and add the following variables:
  ```shell
  CONFLUENCE_API_USER=your-confluence-email
  CONFLUENCE_API_TOKEN=your-confluence-api-token
  CONFLUENCE_SPACE_KEY=your-space-key
  ```
4. Run the script:
  ```shell
  $ python space_exporter.py
  ```

The script will download all pages from the specified Confluence space and save
them in the output directory. It will also generate an all_pages.csv file with
metadata about each page.

### Output Structure

- HTML and JSON Files:
  - The script saves HTML and JSON versions of each page in the `output/html` and `output/json` directories, respectively.
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
