-----

# Multi-Site Price Tracker 📉..

An automated web scraping application that tracks product prices from multiple e-commerce websites, saves the price history to an SQLite database, and runs on a daily schedule.

-----

## Features

  * **Multi-Site Support**: Scrapes data from different websites like Amazon, Flipkart, and Croma.
  * **Configuration-Driven**: Easily add new products or websites by editing simple JSON configuration files.
  * **Automated Scheduling**: Uses the `schedule` library to automatically check prices at a set time every day.
  * **Database Storage**: All price history is stored in a structured SQLite database (`prices.db`).

-----

## Prerequisites

  * Python 3.8+
  * `uv` package manager installed.

-----

## Setup & Configuration

1.  **Clone the Repository**

    ```bash
    git clone https://github.com/HackSmith010/Automated_price_tracker.git
    cd Automated_price_tracker
    ```

2.  **Install Dependencies**
    This command reads the `pyproject.toml` file to  install the necessary packages (`requests`, `beautifulsoup4`, `schedule`).

    ```bash
    uv pip sync
    ```

3.  **Configure Products to Track**
    Open the `products.json` file and add the URLs of the products you wish to track.

    ```json
    [
        {
            "url": "https://www.amazon.in/..."
        },
        {
            "url": "https://www.flipkart.com/..."
        }
    ]
    ```

4.  **Configure Site Scrapers (Optional)**
    If a website changes its layout, you can update the scraping rules in the `site_configs.json` file. To add a new site, simply add a new entry with its domain and the correct HTML selectors for the title and price.

-----

## Usage

To start the automated tracker, run the `main.py` script from your terminal.

```bash
uv run main.py
```

The script will:

1.  Run the tracking job once immediately upon startup.
2.  Continue running in the background to check for prices at the scheduled time every day.

**Note**: The terminal window must remain open for the scheduler to function.

-----

## Viewing the Data

All scraped data is stored in the `prices.db` file. You can view this data in two ways:

#### **1. Using a GUI Tool (Recommended)**

Download and use a free tool like **DB Browser for SQLite** to open the `prices.db` file and browse the data in a spreadsheet-like interface.

#### **2. Using the Terminal**

You can query the database directly from your terminal.

```bash
# Open the database
sqlite3 prices.db

# Run a query to see all data
sqlite> .headers on
sqlite> .mode column
sqlite> SELECT * FROM prices;

# Exit the shell
sqlite> .quit
```
