import schedule
import time
import requests
import os
from predictor import get_market_data, predict_5min
from datetime import datetime
from dotenv import load_dotenv

load_dotenv('/root/ClawClue/.env')

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

COINS = ["BTC", "ETH", "SOL"]

def send_telegram(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message,
        "parse_mode": "HTML"
    }
    try:
        requests.post(url, json=payload, timeout=10)
    except Exception as e:
        print(f"  Telegram error: {e}")

def predict_coin(coin):
    print(f"\n{'='*50}")
    print(f"🔮 Predicting {coin} — {datetime.now().strftime('%H:%M:%S')}")
    print(f"{'='*50}")

    market_data, thread_id = get_market_data(coin)

    response_text = (
        market_data.get("result") or
        market_data.get("output") or
        market_data.get("response") or
        str(market_data)
    )
    print(f"  Data: {str(response_text)[:150]}...")

    prediction = predict_5min(coin, thread_id)

    pred_text = (
        prediction.get("result") or
        prediction.get("output") or
        prediction.get("response") or
        prediction.get("message") or
        str(prediction)
    )

    print(f"\n🎯 {coin} PREDICTION: {pred_text}")

    if pred_text and "jobId" not in str(pred_text) and len(str(pred_text)) < 500:
        return pred_text
    else:
        print(f"  ⚠️ {coin} result not clean, skipping.")
        return None

def run_clawclue():
    print(f"\n{'='*50}")
    print(f"🚀 ClawClue Running — {datetime.now().strftime('%H:%M:%S')} UTC+8")
    print(f"{'='*50}")

    now = datetime.now().strftime('%H:%M:%S')
    results = {}

    for coin in COINS:
        pred = predict_coin(coin)
        if pred:
            results[coin] = pred
        time.sleep(3)

    if results:
        msg = f"🔮 <b>ClawClue Signal</b> — {now} UTC+8\n"
        msg += f"{'='*30}\n\n"

        icons = {"BTC": "₿", "ETH": "⟠", "SOL": "◎"}
        for coin, pred in results.items():
            msg += f"{icons.get(coin, '🪙')} <b>{coin}</b> (5 min)\n"
            msg += f"{pred}\n\n"

        msg += f"🌐 clawclue.com"

        send_telegram(msg)
        print("\n✅ Signal sent to Telegram!")

        with open("predictions_log.txt", "a") as f:
            for coin, pred in results.items():
                f.write(f"{datetime.now()} | {coin} | {pred}\n")
    else:
        print("\n⚠️ No clean results to send.")

schedule.every(5).minutes.do(run_clawclue)

if __name__ == "__main__":
    print("🚀 ClawClue Agent started!")
    send_telegram(
        "🚀 <b>ClawClue Agent started!</b>\n"
        "Predicting BTC, ETH & SOL every 5 minutes...\n"
        "🌐 clawclue.com"
    )
    run_clawclue()
    while True:
        schedule.run_pending()
        time.sleep(1)
