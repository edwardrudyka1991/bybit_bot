
import os import requests import time import logging from datetime import datetime import hmac import hashlib import json

logging.basicConfig(level=logging.INFO)

API_KEY = os.getenv("BYBIT_API_KEY") API_SECRET = os.getenv("BYBIT_API_SECRET")

BASE_URL = "https://api.bybit.com" SYMBOLS = ["BTCUSDT", "ETHUSDT", "SOLUSDT", "XRPUSDT"] TIMEFRAME = "15" LIMIT = 100

def get_signature(params, secret): param_str = "&".join(f"{key}={value}" for key, value in sorted(params.items())) return hmac.new(bytes(secret, "utf-8"), bytes(param_str, "utf-8"), hashlib.sha256).hexdigest()

def get_klines(symbol): endpoint = "/v5/market/kline" url = BASE_URL + endpoint params = { "category": "linear", "symbol": symbol, "interval": TIMEFRAME, "limit": LIMIT } try: response = requests.get(url, params=params, timeout=10) if response.status_code != 200: logging.error(f"{symbol} | HTTP {response.status_code}: {response.text}") return None

data = response.json()
    if data.get("retCode") != 0:
        logging.error(f"{symbol} | Bybit API помилка: {data}")
        return None

    return data["result"]["list"]
except Exception as e:
    logging.error(f"{symbol} | Виняток: {e}")
    return None

def calculate_rsi(close_prices, period=14): gains = [] losses = [] for i in range(1, len(close_prices)): delta = close_prices[i] - close_prices[i - 1] if delta >= 0: gains.append(delta) losses.append(0) else: gains.append(0) losses.append(abs(delta))

avg_gain = sum(gains[:period]) / period
avg_loss = sum(losses[:period]) / period

for i in range(period, len(gains)):
    avg_gain = (avg_gain * (period - 1) + gains[i]) / period
    avg_loss = (avg_loss * (period - 1) + losses[i]) / period

rs = avg_gain / avg_loss if avg_loss != 0 else 0
rsi = 100 - (100 / (1 + rs))
return rsi

def main_loop(): while True: for symbol in SYMBOLS: data = get_klines(symbol) if not data: logging.warning(f"Не вдалось отримати дані для {symbol}") continue

close_prices = [float(entry[4]) for entry in reversed(data)]
        rsi = calculate_rsi(close_prices)
        logging.info(f"[{datetime.now()}] {symbol} RSI: {rsi:.2f}")

    time.sleep(60)

if name == "main": main_loop()


