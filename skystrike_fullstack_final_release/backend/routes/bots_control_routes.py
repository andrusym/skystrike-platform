from fastapi import APIRouter, HTTPException
import subprocess

router = APIRouter()

@router.post("/bots/trigger/{bot_name}")
def trigger_bot(bot_name: str):
    try:
        result = subprocess.run(
            ["python3", "bots/runner_dispatcher.py", bot_name],
            capture_output=True,
            text=True,
            check=True
        )
        return {
            "message": f"Bot '{bot_name}' triggered.",
            "output": result.stdout
        }
    except subprocess.CalledProcessError as e:
        raise HTTPException(status_code=500, detail=f"Bot error: {e.stderr}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
