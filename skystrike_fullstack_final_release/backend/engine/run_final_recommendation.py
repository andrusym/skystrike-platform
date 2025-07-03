# backend/engine/run_final_recommendation.py

from engine import generate_final_recommendation

if __name__ == "__main__":
    print("? Running final portfolio recommendation...")
    result = generate_final_recommendation()
    print("? Final recommendation generated:")
    print(result)
