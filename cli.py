import argparse
import os
import sys
from typing import Any, Dict

from dotenv import load_dotenv

from bot.client import BinanceAPIError, BinanceFuturesClient
from bot.logging_config import setup_logger
from bot.orders import OrderService
from bot.validators import ValidationError


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Simplified Binance Futures Testnet trading bot"
    )
    parser.add_argument("--symbol", required=True, help="Trading pair, e.g., BTCUSDT")
    parser.add_argument("--side", required=True, choices=["BUY", "SELL", "buy", "sell"], help="BUY or SELL")
    parser.add_argument("--type", required=True, choices=["MARKET", "LIMIT", "market", "limit"], help="MARKET or LIMIT")
    parser.add_argument("--quantity", required=True, help="Order quantity, e.g., 0.001")
    parser.add_argument("--price", help="Required for LIMIT orders, e.g., 60000")
    parser.add_argument("--log-file", default="logs/trading_bot.log", help="Path to log file")
    return parser


def print_summary(params: Dict[str, Any]) -> None:
    print("\nOrder Request Summary")
    print("-" * 24)
    for key, value in params.items():
        print(f"{key}: {value}")


def print_response(response: Dict[str, Any]) -> None:
    print("\nOrder Response Details")
    print("-" * 24)
    print(f"orderId: {response.get('orderId', 'N/A')}")
    print(f"status: {response.get('status', 'N/A')}")
    print(f"executedQty: {response.get('executedQty', 'N/A')}")
    print(f"avgPrice: {response.get('avgPrice', 'N/A')}")
    print("\nSuccess: Order request completed on Binance Futures Testnet.")


def main() -> int:
    load_dotenv()
    args = build_parser().parse_args()
    logger = setup_logger(args.log_file)

    try:
        client = BinanceFuturesClient(
            api_key=os.getenv("BINANCE_API_KEY", ""),
            api_secret=os.getenv("BINANCE_API_SECRET", ""),
            base_url=os.getenv("BINANCE_BASE_URL", "https://testnet.binancefuture.com"),
            logger=logger,
        )
        service = OrderService(client, logger)
        params = service.build_order_params(args.symbol, args.side, args.type, args.quantity, args.price)
        print_summary(params)
        response = client.create_order(**params)
        print_response(response)
        return 0

    except ValidationError as exc:
        logger.error("Validation failed | %s", exc)
        print(f"\nFailure: Invalid input - {exc}", file=sys.stderr)
        return 2
    except BinanceAPIError as exc:
        logger.error("API failure | %s", exc)
        print(f"\nFailure: {exc}", file=sys.stderr)
        return 1
    except Exception as exc:
        logger.exception("Unexpected error")
        print(f"\nFailure: Unexpected error - {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
