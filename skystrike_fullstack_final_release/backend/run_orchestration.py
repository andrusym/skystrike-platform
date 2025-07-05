import sys
import os
import traceback

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from backend.engine.orchestration_engine import orchestrate

if __name__ == "__main__":
    try:
        print("🚀 Running scheduled orchestration...")
        result = orchestrate()
        print("✅ Orchestration complete.")
    except Exception as e:
        print("❌ Orchestration failed:")
        traceback.print_exc()