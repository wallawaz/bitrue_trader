import argparse
import os
import time

from bitrue import Bitrue


parser = argparse.ArgumentParser()
parser.add_argument("symbol", help="desired symbol to enter the market with")
parser.add_argument("quote_asset", help="quote asset symbol is traded with")
args = parser.parse_args()


client = Bitrue(
    api_key=os.getenv("BITRUE_API_KEY"),
    api_secret=os.getenv("BITRUE_API_SECRET")
)

symbol_match_string = args.symbol.upper() + args.quote_asset.upper()
found = False
# continously look for given signal
while not found:
    print(f"Looking for: {args.symbol} using {args.quote_asset}")
    exchange_info = client.exchange_info()
    symbols = exchange_info["symbols"]

    # `symbol` payload is formatted as:
    #  <symbol>+<quoteasset>
    # IE: {
    #  'symbol': 'ZAPXRP',
    #  'status': 'TRADING',
    #  'baseAsset': 'zap',
    #  'quoteAsset': 'xrp'
    #   ....
    #  }
    for s in symbols:
        if symbol_match_string == s["symbol"]:
            print("Found!")
            found = True
            print("Placing orders...")
            break
    else:
        print("Not found. sleeping 10s.")
        time.sleep(10)
