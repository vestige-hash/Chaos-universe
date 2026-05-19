# Chaos Universe - Automated Stock Price Updater

Automatically fetches closing stock prices and updates your Google Sheet. No more manual price updates!

## Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Set Up Google Cloud Credentials

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project (or use existing)
3. Enable the **Google Sheets API** and **Google Drive API**
4. Create a Service Account:
   - Go to "IAM & Admin" → "Service Accounts"
   - Click "Create Service Account"
   - Give it a name like "stock-price-updater"
   - Click "Create and Continue" (skip optional steps)
5. Create a key:
   - Click on the service account you just created
   - Go to "Keys" tab → "Add Key" → "Create new key"
   - Choose JSON format
   - Download and save as `credentials.json` in this directory
6. Share your Google Sheet with the service account email (found in the JSON file)

### 3. Configure

Edit `config.py` to set your:
- `SHEET_ID` - The ID from your Google Sheet URL
- `WORKSHEET_NAME` - The tab name for stock tracking
- `DEFAULT_TICKERS` - Your stock tickers

### 4. Initialize the Sheet

```bash
python setup_sheet.py
```

This creates the proper columns and formulas for P&L tracking.

### 5. Run the Updater

**One-time update:**
```bash
python stock_price_updater.py
```

**Set entry prices (run once when starting a new position):**
```bash
python stock_price_updater.py --update-entries
```

**Dry run (see what would happen without making changes):**
```bash
python stock_price_updater.py --dry-run
```

**Continuous mode (updates every hour):**
```bash
python stock_price_updater.py --schedule
```

## Automated Scheduling

### Option 1: Cron Job (Linux/Mac)

Add to your crontab (`crontab -e`):

```cron
# Update stock prices every hour during market hours (9 AM - 5 PM ET, Mon-Fri)
0 9-17 * * 1-5 cd /path/to/Chaos-universe && python stock_price_updater.py >> /var/log/stock-updater.log 2>&1

# Update once at end of day for closing prices
0 18 * * 1-5 cd /path/to/Chaos-universe && python stock_price_updater.py >> /var/log/stock-updater.log 2>&1
```

### Option 2: GitHub Actions

Create `.github/workflows/update-prices.yml`:

```yaml
name: Update Stock Prices

on:
  schedule:
    # Run at 6 PM ET (22:00 UTC) on weekdays
    - cron: '0 22 * * 1-5'
  workflow_dispatch:  # Allow manual trigger

jobs:
  update:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'

      - name: Install dependencies
        run: pip install -r requirements.txt

      - name: Update prices
        env:
          GOOGLE_CREDENTIALS: ${{ secrets.GOOGLE_CREDENTIALS }}
        run: |
          echo "$GOOGLE_CREDENTIALS" > credentials.json
          python stock_price_updater.py
```

Then add your credentials.json content as a GitHub secret named `GOOGLE_CREDENTIALS`.

### Option 3: systemd Timer (Linux)

Create `/etc/systemd/system/stock-updater.service`:
```ini
[Unit]
Description=Stock Price Updater

[Service]
Type=oneshot
WorkingDirectory=/path/to/Chaos-universe
ExecStart=/usr/bin/python3 stock_price_updater.py
User=youruser
```

Create `/etc/systemd/system/stock-updater.timer`:
```ini
[Unit]
Description=Run Stock Price Updater at market close

[Timer]
OnCalendar=Mon-Fri 18:00
Persistent=true

[Install]
WantedBy=timers.target
```

Enable with:
```bash
sudo systemctl enable stock-updater.timer
sudo systemctl start stock-updater.timer
```

## Sheet Structure

The updater expects/creates this structure:

| Ticker | Entry Price | Current Price | Last Updated | P&L % | P&L $ | Notes |
|--------|-------------|---------------|--------------|-------|-------|-------|
| NVDA   | $223.38     | $220.15       | 2026-05-19   | -1.4% | -$3.23|       |
| DELL   | $233.78     | $239.20       | 2026-05-19   | +2.3% | +$5.42|       |

- **Ticker**: Stock symbol (read by updater)
- **Entry Price**: Your buy price (set once with `--update-entries` or manually)
- **Current Price**: Latest closing price (auto-updated)
- **Last Updated**: Timestamp of last update (auto-updated)
- **P&L %**: Calculated automatically via formula
- **P&L $**: Calculated automatically via formula

## Troubleshooting

**"Credentials file not found"**
- Download your service account JSON and save it as `credentials.json`

**"Worksheet not found"**
- Check `WORKSHEET_NAME` in config.py matches your sheet tab name
- Run `setup_sheet.py` to create the worksheet

**"Permission denied" on Google Sheet**
- Share the sheet with the service account email (ends in `@*.iam.gserviceaccount.com`)
- Give "Editor" access

**"No data found for ticker"**
- Verify the ticker symbol is correct (use Yahoo Finance symbols)
- Some tickers may be delisted or have different symbols
