import requests
import os
import json

BASE_URL = os.getenv("API_URL", "http://localhost:8000/api")
USERNAME = os.getenv("API_USER", "admin")
PASSWORD = os.getenv("API_PASS", "admin123")

def authenticate():
    try:
        res = requests.post(f"{BASE_URL}/login", json={"username": USERNAME, "password": PASSWORD})
        if res.status_code == 200:
            token = res.json().get("access_token")
            print("🔐 Authenticated successfully.")
            return token
        else:
            print(f"❌ Auth failed: {res.status_code} - {res.text}")
            return None
    except Exception as e:
        print(f"❌ Auth exception: {str(e)}")
        return None

def check_endpoint(path, token, method="GET", payload=None):
    url = f"{BASE_URL}{path}"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    try:
        if method == "GET":
            res = requests.get(url, headers=headers)
        elif method == "POST":
            res = requests.post(url, headers=headers, json=payload or {})
        else:
            return False, f"{path} ✗ Unsupported method"

        if res.status_code == 200:
            return True, f"{path} ✅"
        else:
            return False, f"{path} ❌ {res.status_code} - {res.text}"
    except Exception as e:
        return False, f"{path} ❌ Exception - {str(e)}"

def main():
    token = authenticate()
    if not token:
        return

    routes = [
        ("/health", "GET"),
        ("/dashboard", "GET"),
        ("/bots/status", "GET"),
        ("/orders/open", "GET"),
        ("/orders/history", "GET"),
        ("/orders/status/test-id", "GET"),  # Should handle 404 gracefully
        ("/lifecycle", "GET"),
        ("/fallbacks", "GET"),
        ("/portfolio/final-recommendation", "GET"),
        ("/wealth/overview", "GET"),
        ("/ml/status", "GET"),
        ("/trades", "GET")
    ]

    print("\n🚦 SkyStrike API Startup Validation Report")
    all_passed = True
    for route, method in routes:
        success, message = check_endpoint(route, token, method)
        print(message)
        if not success:
            all_passed = False

    if all_passed:
        print("\n✅ ALL CHECKS PASSED.")
    else:
        print("\n❌ ONE OR MORE CHECKS FAILED.")

if __name__ == "__main__":
    main()