#!/bin/bash
cd /home/ubuntu/skystrike_fullstack_final_release/backend
source venv/bin/activate
python3 scripts/run_active_bots.py
python3 scripts/run_wealth_engine.py
