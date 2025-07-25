import os
import time
import logging
import asyncio
from telegram import Bot
from pybit.unified_trading import HTTP
from datetime import datetime
import numpy as np

# === Telegram Config ===
TELEGRAM_TOKEN = "8357826174:AAE9HWW65FM2YeZMaW3delIFDTuMdXzv8vg"
TELEGRAM_USER_ID = 343026365

# === Bybit Config ===
session = HTTP(testnet=False)

# === Торгова логіка ===
symbol
