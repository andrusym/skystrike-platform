import requests
import os

BASE_URL = os.getenv("API_URL", "http://localhost:8000/api")
USERNAME = os.getenv("API_USER", "admin")
PASSWORD = os.getenv("API_PASS", "admin123")

def authenticate():
    try:
        res = requests.post(f"{BASE_URL}/login", json={"username": USERNAME, "password": PASSWORD})
        if res.status_code == 200:
            print("🔐 Authenticated.")
            return res.json().get("access_token")
        else:
            print(f"❌ Auth failed: {res.status_code} - {res.text}")
            return None
    except Exception as e:
        print(f"❌ Auth error: {str(e)}")
        return None

def safe_get(path, token):
    try:
        res = requests.get(f"{BASE_URL}{path}", headers={"Authorization": f"Bearer {token}"})
        return res.status_code, res.json()
    except Exception as e:
        return 500, {"error": str(e)}

def check_dashboard(data):
    checks = {
        "openPnL": data.get("openPnL", -1) is not None,
        "netPnL": data.get("netPnL", -1) is not None,
        "winRate": data.get("winRate", -1) >= 0,
        "mlEngine.status": data.get("mlEngine", {}).get("status") in ["online", "degraded"],
        "capital.allocated": data.get("capital", {}).get("allocated", 0) > 0
    }
    return checks

def main():
    token = authenticate()
    if not token:
        return

    print("\n🔍 API Status Report")

    endpoints = ["/health", "/ml/status", "/portfolio/final-recommendation", "/dashboard"]
    for ep in endpoints:
        code, data = safe_get(ep, token)
        print(f"{ep} -> {code}")
        if ep == "/dashboard" and code == 200:
            dashboard_checks = check_dashboard(data)
            for k, v in dashboard_checks.items():
                print(f"  {k}: {'✅' if v else '❌'}")

if __name__ == "__main__":
    main()