import requests
import os
import time
from dotenv import load_dotenv

load_dotenv('/root/ClawClue/.env')

API_KEY = os.getenv("BANKR_API_KEY")
API_URL = os.getenv("BANKR_API_URL")
HEADERS = {
    "X-API-Key": API_KEY,
    "Content-Type": "application/json"
}

def submit_prompt(prompt, thread_id=None):
    payload = {"prompt": prompt}
    if thread_id:
        payload["threadId"] = thread_id
    res = requests.post(API_URL + "/agent/prompt", headers=HEADERS, json=payload)
    data = res.json()
    job_id = data.get("jobId")
    thread_id = data.get("threadId")
    print("  Job ID: " + str(job_id))
    for _ in range(60):
        result = requests.get(API_URL + "/agent/job/" + str(job_id), headers=HEADERS).json()
        status = result.get("status")
        updates = result.get("statusUpdates", [])
        if updates:
            print("  >> " + updates[-1].get("message", ""))
        if status == "completed":
            print("  Final: completed")
            return result, thread_id
        if status in ["failed", "cancelled"]:
            print("  Final: " + status)
            return result, thread_id
        time.sleep(5)
    return result, thread_id

def get_market_data(coin):
    print(f"  Fetching {coin} data...")
    return submit_prompt(
        f"Using bankr skill, get current {coin} price, RSI, moving averages MA5 and MA10, "
        f"support and resistance levels."
    )

def predict_5min(coin, thread_id):
    print(f"  Predicting {coin}...")
    result, _ = submit_prompt(
        f"Based on the {coin} technical data above, predict UP or DOWN in next 5 minutes. "
        f"Reply ONLY in this exact format: DIRECTION | CONFIDENCE% | REASON",
        thread_id
    )
    return result
