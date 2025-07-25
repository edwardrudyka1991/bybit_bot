import time
import logging
from pybit.unified_trading import HTTP
import requests
from telegram import Bot
from datetime import datetime

# ==== Налаштування ====
TELEGRAM_TOKEN = "8357826174:AAE9HWW65FM2YeZMaW3delIFDTuMdXzv8vg"
TELEGRAM_CHAT_ID = 343026365
API_KEY = "your_bybit_api_key"
API_SECRET = "your_bybit_api_secret"

symbols = ["SOLUSDT", "BTCUSDT", "ETHUSDT", "XRPUSDT"]
RSI_PERIOD = 14
TIMEFRAME = "15"  # 15 хвилин
START_BALANCE = 15
TRADE_PERCENT = 0.10
LEVERAGE = 5

bot = Bot(token=TELEGRAM_TOKEN)
session = HTTP(testnet=True)

def get_rsi(symbol):
    url = f"https://api.bybit.com/v5/market/kline?category=linear&symbol={symbol}&interval={TIMEFRAME}&limit=100"
    try:
        response = requests.get(url)
        data = response.json()

        if "result" not in data or "list" not in data["result"]:
            logging.error(f"❌ Невірна відповідь API для {symbol}: {data}")
            return None

        closes = [float(candle[4]) for candle in data["result"]["list"]]
        if len(closes) < RSI_PERIOD + 1:
            return None

        gains, losses = [], []
        for i in range(1, RSI_PERIOD + 1):
            change = closes[-i] - closes[-i - 1]
            if change > 0:
                gains.append(change)
            else:
                losses.append(abs(change))

        avg_gain = sum(gains) / RSI_PERIOD
        avg_loss = sum(losses) / RSI_PERIOD
        if avg_loss == 0:
            return 100
        rs = avg_gain / avg_loss
        rsi = 100 - (100 / (1 + rs))
        return round(rsi, 2)
    except Exception as e:
        logging.error(f"Помилка з {symbol}: {e}")
        return None

def send_signal(symbol, rsi):
    signal = ""
    if rsi < 30:
        signal = "🟢 LONG"
    elif rsi > 70:
        signal = "🔴 SHORT"
    else:
        return

    amount = round((START_BALANCE * TRADE_PERCENT) * LEVERAGE, 2)
    message = (
        f"📈 {signal} сигнал по {symbol}\n"
        f"RSI: {rsi}\n"
        f"Рекомендована сума входу: ≈ {amount} USDT (з плечем {LEVERAGE}x)"
    )
    bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=message)

def main():
    while True:
        for symbol in symbols:
            try:
                rsi = get_rsi(symbol)
                if rsi:
                    send_signal(symbol, rsi)
                else:
                    logging.warning(f"Не вдалось отримати RSI для {symbol}")
            except Exception as e:
                logging.error(f"Помилка з {symbol}: {e}")
        time.sleep(900)  # 15 хвилин

if __name__ == "__main__":
    main()
