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
    while True:
        result = requests.get(API_URL + "/agent/job/" + str(job_id), headers=HEADERS).json()
        status = result.get("status")
        if status in ["completed", "failed", "cancelled"]:
            print("  Status: " + status)
            return result, thread_id
        time.sleep(2)

def get_btc_data():
    print("  Fetching BTC data...")
    return submit_prompt("Get current BTC price, RSI, moving averages MA5 and MA10, support and resistance levels.")

def predict_5min(thread_id):
    print("  Requesting 5 minute prediction...")
    result, _ = submit_prompt("Based on BTC technical indicators, predict UP or DOWN in next 5 minutes. Format: DIRECTION | CONFIDENCE% | REASON", thread_id)
    return result
