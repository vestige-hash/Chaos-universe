#!/usr/bin/env python3
"""
Setup script to initialize the Google Sheet with proper columns and tickers.
Run this once to prepare the sheet for automated price updates.
"""

import gspread
from google.oauth2.service_account import Credentials
from pathlib import Path

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


def setup_quant_model_sheet():
    """Create or update the Quant Model worksheet with proper structure."""
    print("Connecting to Google Sheets...")
    client = get_google_sheets_client()
    spreadsheet = client.open_by_key(config.SHEET_ID)

    try:
        worksheet = spreadsheet.worksheet(config.WORKSHEET_NAME)
        print(f"Found existing worksheet: {config.WORKSHEET_NAME}")
    except gspread.WorksheetNotFound:
        print(f"Creating new worksheet: {config.WORKSHEET_NAME}")
        worksheet = spreadsheet.add_worksheet(
            title=config.WORKSHEET_NAME,
            rows=20,
            cols=10,
        )

    headers = [
        "Ticker",
        "Entry Price",
        "Current Price",
        "Last Updated",
        "P&L %",
        "P&L $",
        "Notes",
    ]

    print("Setting up headers...")
    worksheet.update("A1:G1", [headers])

    worksheet.format("A1:G1", {
        "textFormat": {"bold": True},
        "backgroundColor": {"red": 0.9, "green": 0.9, "blue": 0.9},
    })

    existing_tickers = worksheet.col_values(1)[1:]

    if not existing_tickers:
        print("Adding default tickers...")
        ticker_data = [[ticker] for ticker in config.DEFAULT_TICKERS]
        worksheet.update(f"A2:A{1 + len(config.DEFAULT_TICKERS)}", ticker_data)

    num_rows = len(existing_tickers) if existing_tickers else len(config.DEFAULT_TICKERS)

    print("Setting up P&L formulas...")
    pnl_formulas = []
    for row in range(2, 2 + num_rows):
        pnl_pct = f'=IF(AND(B{row}<>"",C{row}<>""),(C{row}-B{row})/B{row}*100,"")'
        pnl_dollar = f'=IF(AND(B{row}<>"",C{row}<>""),C{row}-B{row},"")'
        pnl_formulas.append([pnl_pct, pnl_dollar])

    if pnl_formulas:
        worksheet.update(
            f"E2:F{1 + num_rows}",
            pnl_formulas,
            value_input_option="USER_ENTERED",
        )

    worksheet.format(f"B2:C{1 + num_rows}", {"numberFormat": {"type": "CURRENCY"}})
    worksheet.format(f"E2:E{1 + num_rows}", {"numberFormat": {"type": "NUMBER", "pattern": "0.00%"}})
    worksheet.format(f"F2:F{1 + num_rows}", {"numberFormat": {"type": "CURRENCY"}})

    print("\nSheet setup complete!")
    print(f"Spreadsheet URL: https://docs.google.com/spreadsheets/d/{config.SHEET_ID}/edit")
    print("\nNext steps:")
    print("1. Run 'python stock_price_updater.py --update-entries' to set entry prices")
    print("2. Run 'python stock_price_updater.py' to update current prices")
    print("3. Set up a cron job for automated updates (see README.md)")


if __name__ == "__main__":
    setup_quant_model_sheet()
