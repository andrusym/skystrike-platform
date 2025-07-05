import os
import json

BASE_DIR = os.getenv("BACKEND_DIR", "./")

required_files = [
    "config/bot_config.json",
    "config/lifecycle_config.json",
    "config/fallback_config.json",
    "config/portfolio_profiles.json",
    "data/wealth_config.json",
    "users.json",
    "trade_log.json",
    "ml_scores.json"
]

def validate_file(path):
    full_path = os.path.join(BASE_DIR, path)
    if not os.path.exists(full_path):
        return False, f"{path} ❌ MISSING"
    try:
        with open(full_path, "r") as f:
            content = json.load(f)
            if isinstance(content, dict) or isinstance(content, list):
                return True, f"{path} ✅ OK"
            else:
                return False, f"{path} ❌ INVALID FORMAT"
    except Exception as e:
        return False, f"{path} ❌ ERROR - {str(e)}"

def main():
    print("📁 SkyStrike Config File Validator")
    all_passed = True
    for file in required_files:
        ok, msg = validate_file(file)
        print(msg)
        if not ok:
            all_passed = False
    if all_passed:
        print("\n✅ All required files exist and are valid.")
    else:
        print("\n❌ One or more files are missing or invalid.")

if __name__ == "__main__":
    main()