# Falabella Retail Scraper

A Python data engineering project to extract, process, and save product and collection data from Falabella's retail website.

## Features

- Scrapes product and collection data using Selenium and custom request extraction.
- Processes and flattens nested JSON responses.
- Cleans and exports data to CSV for analysis.
- Handles price formatting and preserves string values.
- Logs all process steps to both console and `process.log`.

## Project Structure

- `src/` — Main source code (scraping, data handling, utilities)
- `config/` — Configuration files and URL lists
- `data/` — Cached responses and output data (git-ignored)
- `tests/` — Test scripts

## Usage

1. Install dependencies:
   ```
   uv pip install -r requirements.txt
   ```
2. Configure environment variables and URLs in `config/`.
3. Run the main process:
   ```
   python -m src.main
   ```
4. Output CSVs and logs will be saved in the appropriate folders.

## Notes

- Requires Python 3.8+
- All logs are saved to `process.log` and shown in the console.
- Data and config folders are git-ignored for safety.

---

Made with ❤️ for data engineering and retail analytics.
