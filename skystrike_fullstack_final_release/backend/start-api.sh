#!/bin/bash
cd /home/ubuntu/skystrike_fullstack_final_release
exec uvicorn backend.main:app --host 0.0.0.0 --port 8000
