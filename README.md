# Simplified Binance Futures Testnet Trading Bot

A small Python CLI application that places `MARKET` and `LIMIT` orders on Binance USDT-M Futures Testnet with validation, logging, and reusable code structure.

> This project is for Binance Futures Testnet only. Do not use real mainnet credentials.

## Features

- Places MARKET and LIMIT orders
- Supports BUY and SELL sides
- Validates CLI inputs
- Separates API/client logic from order and CLI logic
- Logs API requests, responses, validation errors, API errors, and network failures
- Keeps credentials outside source code using `.env`

## Project Structure

```text
trading_bot/
  bot/
    __init__.py
    client.py
    orders.py
    validators.py
    logging_config.py
  cli.py
  README.md
  requirements.txt
  .env.example
  logs/
    sample_market_order.log
    sample_limit_order.log
```

## Setup Steps

### 1. Create and activate a virtual environment

```bash
python -m venv .venv
```

Windows:

```bash
.venv\Scripts\activate
```

macOS/Linux:

```bash
source .venv/bin/activate
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Create `.env` file

Copy `.env.example` to `.env`:

```bash
copy .env.example .env
```

On macOS/Linux:

```bash
cp .env.example .env
```

Then add your Binance Futures Testnet credentials:

```env
BINANCE_API_KEY=your_testnet_api_key_here
BINANCE_API_SECRET=your_testnet_api_secret_here
BINANCE_BASE_URL=https://testnet.binancefuture.com
```

## How to Run

Run all commands from the `trading_bot` folder.

### MARKET order example

```bash
python cli.py --symbol BTCUSDT --side BUY --type MARKET --quantity 0.001
```

### LIMIT order example

```bash
python cli.py --symbol BTCUSDT --side SELL --type LIMIT --quantity 0.001 --price 70000
```

### Custom log file example

```bash
python cli.py --symbol BTCUSDT --side BUY --type MARKET --quantity 0.001 --log-file logs/market_order.log
```

## Output Example

```text
Order Request Summary
------------------------
symbol: BTCUSDT
side: BUY
type: MARKET
quantity: 0.001

Order Response Details
------------------------
orderId: 123456789
status: NEW
executedQty: 0.001
avgPrice: 65000.00

Success: Order request completed on Binance Futures Testnet.
```

## Logging

Logs are written to:

```text
logs/trading_bot.log
```

The log file records:

- API request endpoint and parameters
- API response status and body
- validation failures
- Binance API errors
- network failures
- unexpected exceptions

Sample log files are included in the `logs/` folder. Replace them with real logs generated after placing one MARKET and one LIMIT order on your own Binance Futures Testnet account.

## Assumptions

- The app is designed only for Binance USDT-M Futures Testnet.
- API keys are stored in `.env`, not committed to GitHub.
- LIMIT orders use `timeInForce=GTC`.
- The default base URL is set to the task-provided URL: `https://testnet.binancefuture.com`.
- Quantity and price precision depend on the trading symbol. If Binance rejects precision, adjust the value according to the symbol rules.

## Common Errors

### API key error

Check that `.env` exists and contains valid Futures Testnet credentials.

### Price required error

LIMIT orders must include `--price`.

### Precision error

Use a smaller or valid quantity/price precision for the selected symbol.
