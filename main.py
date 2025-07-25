import time
import logging
import requests
from telegram import Bot

Telegram

TELEGRAM_TOKEN = '8357826174:AAE9HWW65FM2YeZMaW3delIFDTuMdXzv8vg' CHAT_ID = 343026365 bot = Bot(token=TELEGRAM_TOKEN)

Параметри

SYMBOLS = ["SOLUSDT", "BTCUSDT", "ETHUSDT", "XRPUSDT"] TIMEFRAME = "15"  # 15-хвилинний таймфрейм LIMIT = 100 LEVERAGE = 5 BALANCE = 15 POSITION_SIZE = BALANCE * 0.1 * LEVERAGE  # 10% від балансу з плечем 5x

logging.basicConfig(level=logging.INFO)

def get_klines(symbol): url = "https://api.bybit.com/v5/market/kline" params = { "category": "linear", "symbol": symbol, "interval": TIMEFRAME, "limit": LIMIT } try: response = requests.get(url, params=params) data = response.json() return [float(kline[4]) for kline in data["result"]["list"]]  # Закриття свічок except Exception as e: logging.error(f"Помилка з {symbol}: {e}") return []

def calculate_rsi(closes, period=14): if len(closes) < period: return None gains, losses = [], [] for i in range(1, period + 1): diff = closes[-i] - closes[-i - 1] if diff > 0: gains.append(diff) else: losses.append(abs(diff)) avg_gain = sum(gains) / period avg_loss = sum(losses) / period if avg_loss == 0: return 100 rs = avg_gain / avg_loss return 100 - (100 / (1 + rs))

def check_signals(): for symbol in SYMBOLS: closes = get_klines(symbol) if not closes or len(closes) < 15: logging.warning(f"Не вдалось отримати RSI для {symbol}") continue

rsi = calculate_rsi(closes)
    if rsi is None:
        continue

    msg = f"{symbol} | RSI: {round(rsi, 2)}"
    if rsi < 30:
        msg += f"\n🔵 LONG сигнал\nВідкрий позицію на ≈ {round(POSITION_SIZE, 2)} USDT"
    elif rsi > 70:
        msg += f"\n🔴 SHORT сигнал\nВідкрий позицію на ≈ {round(POSITION_SIZE, 2)} USDT"
    else:
        continue

    logging.info(msg)
    bot.send_message(chat_id=CHAT_ID, text=msg)

if name == "main": while True: check_signals() time.sleep(60 * 15)  # перевірка кожні 15 хвилин


