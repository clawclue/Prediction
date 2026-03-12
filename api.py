from flask import Flask, jsonify
from flask_cors import CORS
import os
import re

app = Flask(__name__)
CORS(app)

LOG_FILE = os.path.expanduser("~/ClawClue/predictions_log.txt")

def parse_predictions():
    predictions = []
    try:
        with open(LOG_FILE, "r") as f:
            lines = f.readlines()

        for line in reversed(lines):
            line = line.strip()
            if not line:
                continue

            parts = line.split(" | ", 2)
            if len(parts) < 2:
                continue

            timestamp = parts[0].strip()
            direction = parts[1].strip().upper()
            reasoning = parts[2].strip() if len(parts) > 2 else ""

            # Extract confidence if present (e.g. "65%")
            conf_match = re.search(r'(\d+)%', reasoning)
            confidence = int(conf_match.group(1)) if conf_match else None

            # Extract BTC price if present
            price_match = re.search(r'\$([0-9,]+)', reasoning)
            price = price_match.group(0) if price_match else "N/A"

            predictions.append({
                "timestamp": timestamp,
                "direction": direction if direction in ["UP", "DOWN"] else "UP",
                "confidence": confidence,
                "price": price,
                "reasoning": reasoning
            })

            if len(predictions) >= 20:
                break

    except Exception as e:
        return []

    return predictions

@app.route("/api/latest")
def latest():
    predictions = parse_predictions()
    if not predictions:
        return jsonify({"error": "No predictions found"}), 404
    return jsonify(predictions[0])

@app.route("/api/history")
def history():
    predictions = parse_predictions()
    return jsonify(predictions[:8])

@app.route("/api/stats")
def stats():
    predictions = parse_predictions()
    total = len(predictions)
    up = sum(1 for p in predictions if p["direction"] == "UP")
    down = total - up
    return jsonify({
        "total": total,
        "up": up,
        "down": down
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
