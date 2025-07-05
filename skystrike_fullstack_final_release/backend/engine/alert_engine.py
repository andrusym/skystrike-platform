import os
import requests
import json
from datetime import datetime

SLACK_WEBHOOK = os.getenv("SLACK_WEBHOOK_URL", "")

def send_alert(message, level="info", metadata=None):
    timestamp = datetime.utcnow().isoformat()
    payload = {
        "text": f"[{level.upper()}] {message} ({timestamp})"
    }

    if metadata:
        payload["attachments"] = [{
            "text": json.dumps(metadata, indent=2),
            "color": "#36a64f" if level == "info" else "#ff0000"
        }]

    if SLACK_WEBHOOK:
        try:
            r = requests.post(SLACK_WEBHOOK, json=payload)
            r.raise_for_status()
            print(f"📣 Slack alert sent: {message}")
        except Exception as e:
            print(f"⚠️ Failed to send Slack alert: {e}")
    else:
        print(f"🚨 ALERT: {payload['text']}")
        if metadata:
            print(json.dumps(metadata, indent=2))