# Selenium Web Scraping Script

This project contains a Python script that automates the process of registering an account on the CDP website, retrieving company data, and saving the data to text files. The script uses Selenium WebDriver for browser automation and performs various tasks like generating random emails, fetching verification codes, and handling form submissions.

## Prerequisites

- Python 3.x
- Edge WebDriver

## Installation

1. **Clone the repository**:
    ```sh
    git clone https://github.com/samsara24/RPA-for-CDP.git
    cd RPA-for-CDP
    ```

2. **Install the required Python packages**:
    ```sh
    pip install -r requirements.txt
    ```

3. **Download Edge WebDriver**:
    - Ensure you have the Edge WebDriver that matches your Edge browser version.
    - Download it from: [Microsoft Edge WebDriver](https://developer.microsoft.com/en-us/microsoft-edge/tools/webdriver/)
    - Place the WebDriver executable in a known location and update the `EDGE_DRIVER_PATH` constant in the script with the correct path.

## Configuration

Update the following paths in config.ini and constants in the script as needed:

- `EDGE_DRIVER_PATH`: Path to the Edge WebDriver executable.
- `CSV_FILE_PATH`: Path to the input CSV file containing company names.
- `OUTPUT_DIR`: Directory to save the output text files.
- `NOT_FOUND_FILE`: Path to the file where company names not found will be saved.
- `SECRET_PASSWORD`: Password used for account registration.

## Explanation
The script performs the following steps:

- Initializes the Edge WebDriver.
- Update the config file.
- Opens the CDP website.
- Handles cookie consent and regional selection.
- Navigates to the registration page and registers a new account using a randomly generated email.
- Fetches a verification code and completes the registration.
- Opens the search page and processes the list of companies from the CSV file.
- For each company, it searches for the company data, copies the data to the clipboard, and saves it to a text file.
- Updates the CSV file by removing processed companies.
## Notes
- This Web Page can't be used in some region.
- The script includes various wait times to handle page loads and network latency.
- Exception handling is implemented to manage elements not found within a specified time.
- The script assumes that the input CSV file has a column named Longname containing company names.

## Usage

Run the main script:
```sh
python rpa.py

