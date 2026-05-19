"""Configuration for the stock price automation."""

# Google Sheet ID (from the URL)
# Example: https://docs.google.com/spreadsheets/d/SHEET_ID/edit
SHEET_ID = "1msL7sCf165-zBtazpLT3VUkl9twy5rDYBswgPUVWwcI"

# Worksheet name containing the stock picks
WORKSHEET_NAME = "Quant Model"

# Column mappings (1-indexed)
TICKER_COLUMN = 1      # Column A: Stock ticker
ENTRY_PRICE_COLUMN = 2 # Column B: Entry price
CURRENT_PRICE_COLUMN = 3  # Column C: Current/closing price
LAST_UPDATED_COLUMN = 4   # Column D: Last updated timestamp

# Header row (data starts after this)
HEADER_ROW = 1

# Tickers to track (will also be read from sheet if present)
DEFAULT_TICKERS = [
    "DELL",
    "NVDA",
    "TSM",
    "AMD",
    "SOUN",
    "META",
    "CPRX",
    "ZM",
    "PLTR",
]

# Path to Google service account credentials JSON
CREDENTIALS_PATH = "credentials.json"

# Update schedule (for continuous mode)
UPDATE_INTERVAL_MINUTES = 60
