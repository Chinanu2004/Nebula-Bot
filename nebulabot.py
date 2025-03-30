import requests
import time
import telebot

# === BOT CONFIGURATION ===
BOT_TOKEN = "7674604943:AAFRN2aE12iIx2uiLUiuX-2g_5H6qTN3u6k"
CHAT_ID = "5755854504"
API_KEY = "f8447396-99cb-4918-b26b-41d1c5d40fb3"  # Your trading API key

bot = telebot.TeleBot(BOT_TOKEN)

# === FUNCTION: Fetch Trading Signals ===
def get_trading_signal():
    url = f"https://api.yourtradingplatform.com/signals"
    headers = {"Authorization": f"Bearer {API_KEY}"}

    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()  # Raise exception for HTTP errors (e.g., 404, 500)
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching trading signals: {e}")
        return None

# === FUNCTION: Scan Token ===
def scan_token(token_address):
    url = f"https://api.yourtradingplatform.com/scan/{token_address}"
    headers = {"Authorization": f"Bearer {API_KEY}"}

    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error scanning token: {e}")
        return None

# === TELEGRAM COMMANDS ===
@bot.message_handler(commands=["start"])
def start(message):
    bot.send_message(message.chat.id, "🚀 Welcome to *Nebula*! I provide top trading signals & market insights.\n\nUse:\n- `/signal` to get new trade signals\n- `/scan <token_address>` to check a token’s details.", parse_mode="Markdown")

@bot.message_handler(commands=["signal"])
def send_signal(message):
    signal = get_trading_signal()
    if signal:
        bot.send_message(
            CHAT_ID,
            f"🚀 *New Trading Signal!*\n\n"
            f"🔹 *Token:* {signal.get('token', 'N/A')}\n"
            f"📈 *Expected Gain:* {signal.get('profit', 'N/A')}x\n"
            f"⚠️ *Risk Level:* {signal.get('risk', 'N/A')}",
            parse_mode="Markdown"
        )
    else:
        bot.send_message(CHAT_ID, "⚠️ No signals available at the moment. Try again later.")

@bot.message_handler(commands=["scan"])
def scan(message):
    try:
        token_address = message.text.split(" ")[1]  # Extract token address from command
    except IndexError:
        bot.send_message(CHAT_ID, "❌ Please provide a token address. Example: `/scan 0x123...`", parse_mode="Markdown")
        return
    
    token_info = scan_token(token_address)
    if token_info:
        bot.send_message(
            CHAT_ID,
            f"🔍 *Token Analysis:*\n\n"
            f"🪙 *Token:* {token_info.get('name', 'N/A')}\n"
            f"💰 *Market Cap:* ${token_info.get('market_cap', 'N/A')}\n"
            f"📊 *ATH:* ${token_info.get('ath', 'N/A')}\n"
            f"⚠️ *Risk Level:* {token_info.get('risk_level', 'N/A')}",
            parse_mode="Markdown"
        )
    else:
        bot.send_message(CHAT_ID, "⚠️ Could not fetch token details. Check the address and try again.")

# === RUN THE BOT ===
print("🚀 Nebula Bot is running...")
bot.polling(none_stop=True, timeout=60)
