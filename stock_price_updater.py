#!/usr/bin/env python3
"""
Automated stock closing price updater for Google Sheets.

Fetches current/closing prices for tracked stocks and updates the Google Sheet.
Can be run as a one-shot command or scheduled continuously.
"""

import argparse
import sys
from datetime import datetime
from pathlib import Path

import gspread
import yfinance as yf
from google.oauth2.service_account import Credentials

import config


def get_google_sheets_client():
    """Authenticate and return a gspread client."""
    scopes = [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive",
    ]

    creds_path = Path(config.CREDENTIALS_PATH)
    if not creds_path.exists():
        raise FileNotFoundError(
            f"Credentials file not found: {config.CREDENTIALS_PATH}\n"
            "Please download your service account JSON from Google Cloud Console "
            "and save it as 'credentials.json'"
        )

    credentials = Credentials.from_service_account_file(
        config.CREDENTIALS_PATH,
        scopes=scopes,
    )
    return gspread.authorize(credentials)


def fetch_closing_prices(tickers: list[str]) -> dict[str, dict]:
    """
    Fetch the latest closing prices for a list of tickers.

    Returns dict mapping ticker to price info:
    {
        "AAPL": {"price": 185.50, "date": "2026-05-19", "error": None},
        "INVALID": {"price": None, "date": None, "error": "Ticker not found"},
    }
    """
    results = {}

    for ticker in tickers:
        try:
            stock = yf.Ticker(ticker)
            hist = stock.history(period="5d")

            if hist.empty:
                results[ticker] = {
                    "price": None,
                    "date": None,
                    "error": f"No data found for {ticker}",
                }
                continue

            latest_close = hist["Close"].iloc[-1]
            latest_date = hist.index[-1].strftime("%Y-%m-%d")

            results[ticker] = {
                "price": round(float(latest_close), 2),
                "date": latest_date,
                "error": None,
            }

        except Exception as e:
            results[ticker] = {
                "price": None,
                "date": None,
                "error": str(e),
            }

    return results


def get_tickers_from_sheet(worksheet) -> list[str]:
    """Read tickers from the first column of the sheet."""
    ticker_col = worksheet.col_values(config.TICKER_COLUMN)
    tickers = [t.strip().upper() for t in ticker_col[config.HEADER_ROW:] if t.strip()]
    return tickers


def update_sheet_prices(worksheet, prices: dict[str, dict], dry_run: bool = False):
    """Update the Google Sheet with fetched prices."""
    ticker_col = worksheet.col_values(config.TICKER_COLUMN)
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    updates = []

    for row_idx, ticker in enumerate(ticker_col, start=1):
        if row_idx <= config.HEADER_ROW:
            continue

        ticker = ticker.strip().upper()
        if ticker not in prices:
            continue

        price_info = prices[ticker]
        if price_info["price"] is None:
            print(f"  Skipping {ticker}: {price_info['error']}")
            continue

        price_cell = gspread.utils.rowcol_to_a1(row_idx, config.CURRENT_PRICE_COLUMN)
        timestamp_cell = gspread.utils.rowcol_to_a1(row_idx, config.LAST_UPDATED_COLUMN)

        updates.append({
            "range": price_cell,
            "values": [[price_info["price"]]],
        })
        updates.append({
            "range": timestamp_cell,
            "values": [[timestamp]],
        })

        print(f"  {ticker}: ${price_info['price']} (as of {price_info['date']})")

    if dry_run:
        print("\n[DRY RUN] No changes made to sheet.")
        return

    if updates:
        worksheet.batch_update(updates)
        print(f"\nUpdated {len(updates) // 2} stock prices in sheet.")
    else:
        print("\nNo updates to make.")


def update_entry_prices(worksheet, prices: dict[str, dict], dry_run: bool = False):
    """Update entry prices with current closing prices (one-time setup)."""
    ticker_col = worksheet.col_values(config.TICKER_COLUMN)
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    updates = []

    for row_idx, ticker in enumerate(ticker_col, start=1):
        if row_idx <= config.HEADER_ROW:
            continue

        ticker = ticker.strip().upper()
        if ticker not in prices:
            continue

        price_info = prices[ticker]
        if price_info["price"] is None:
            print(f"  Skipping {ticker}: {price_info['error']}")
            continue

        entry_cell = gspread.utils.rowcol_to_a1(row_idx, config.ENTRY_PRICE_COLUMN)

        updates.append({
            "range": entry_cell,
            "values": [[price_info["price"]]],
        })

        print(f"  {ticker}: Entry price set to ${price_info['price']}")

    if dry_run:
        print("\n[DRY RUN] No changes made to sheet.")
        return

    if updates:
        worksheet.batch_update(updates)
        print(f"\nSet entry prices for {len(updates)} stocks.")


def run_update(update_entries: bool = False, dry_run: bool = False):
    """Main update routine."""
    print(f"Stock Price Updater - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("-" * 50)

    print("Connecting to Google Sheets...")
    client = get_google_sheets_client()
    spreadsheet = client.open_by_key(config.SHEET_ID)

    try:
        worksheet = spreadsheet.worksheet(config.WORKSHEET_NAME)
    except gspread.WorksheetNotFound:
        print(f"Worksheet '{config.WORKSHEET_NAME}' not found.")
        print(f"Available worksheets: {[ws.title for ws in spreadsheet.worksheets()]}")
        print("Please update WORKSHEET_NAME in config.py")
        sys.exit(1)

    print("Reading tickers from sheet...")
    tickers = get_tickers_from_sheet(worksheet)

    if not tickers:
        print("No tickers found in sheet. Using defaults from config.")
        tickers = config.DEFAULT_TICKERS

    print(f"Fetching prices for {len(tickers)} stocks: {', '.join(tickers)}")
    prices = fetch_closing_prices(tickers)

    if update_entries:
        print("\nUpdating ENTRY prices:")
        update_entry_prices(worksheet, prices, dry_run)
    else:
        print("\nUpdating CURRENT prices:")
        update_sheet_prices(worksheet, prices, dry_run)

    print("-" * 50)
    print("Done!")


def run_scheduled():
    """Run updates on a schedule."""
    import schedule
    import time

    print(f"Starting scheduled updates every {config.UPDATE_INTERVAL_MINUTES} minutes")
    print("Press Ctrl+C to stop.\n")

    run_update()

    schedule.every(config.UPDATE_INTERVAL_MINUTES).minutes.do(run_update)

    while True:
        schedule.run_pending()
        time.sleep(60)


def main():
    parser = argparse.ArgumentParser(
        description="Automated stock closing price updater for Google Sheets"
    )
    parser.add_argument(
        "--schedule",
        action="store_true",
        help="Run continuously on a schedule",
    )
    parser.add_argument(
        "--update-entries",
        action="store_true",
        help="Update ENTRY prices instead of current prices (one-time setup)",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Fetch prices but don't update the sheet",
    )

    args = parser.parse_args()

    if args.schedule:
        run_scheduled()
    else:
        run_update(update_entries=args.update_entries, dry_run=args.dry_run)


if __name__ == "__main__":
    main()
