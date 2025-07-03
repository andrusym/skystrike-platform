
# behavioral_nudges.py

import random
import logging

NUDGES = [
    "Consider locking in gains once you're up 30%+.",
    "Review trailing stop placements on wide-wing trades.",
    "Check position sizing during high VIX days.",
    "Avoid revenge trading — reassess after losses."
]

def get_nudge():
    nudge = random.choice(NUDGES)
    logging.info(f"[Nudge] {nudge}")
    return nudge
