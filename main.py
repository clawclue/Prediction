import schedule
import time
from predictor import get_btc_data, predict_5min
from datetime import datetime

def run_clawclue():
    print("\n" + "="*50)
    print(f"🔮 ClawClue Running — {datetime.now().strftime('%H:%M:%S')}")
    print("="*50)

    print("📊 Fetching BTC data from Bankr...")
    market_data, thread_id = get_btc_data()

    response_text = (
        market_data.get("result") or
        market_data.get("output") or
        market_data.get("response") or
        str(market_data)
    )
    print(f"Data: {str(response_text)[:200]}...")

    print("\n🧠 Analyzing for 5 minute prediction...")
    prediction = predict_5min(thread_id)

    pred_text = (
        prediction.get("result") or
        prediction.get("output") or
        prediction.get("response") or
        prediction.get("message") or
        str(prediction)
    )

    print(f"\n🎯 CLAWCLUE PREDICTION:")
    print(pred_text)

    with open("predictions_log.txt", "a") as f:
        f.write(f"{datetime.now()} | {pred_text}\n")

    print("\n✅ Prediction saved to predictions_log.txt")

schedule.every(5).minutes.do(run_clawclue)

if __name__ == "__main__":
    print("🚀 ClawClue Agent started!")
    run_clawclue()
    while True:
        schedule.run_pending()
        time.sleep(1)
