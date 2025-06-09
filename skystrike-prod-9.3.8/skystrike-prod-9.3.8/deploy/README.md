# SkyStrike v7 Deployment Guide

This project includes a full backend (FastAPI + ML strategy engine) and a React-based frontend.

## 🚀 Deployment Using Docker

### Prerequisites
- Docker and Docker Compose installed
- Valid Tradier API key (set in `.env` file under `TRADIER_API_KEY`)

---

### 🔧 File Structure

```
skystrike-v7/
├── backend/
│   ├── main.py
│   ├── strategy_engine.py
│   ├── .env
│   └── Dockerfile
├── frontend/
│   ├── App.jsx
│   ├── ...
├── deploy/
│   ├── docker-compose.yml
│   └── README.md
```

---

### 🔥 Start the Stack

From the root `skystrike-v7/` directory:

```bash
docker-compose -f deploy/docker-compose.yml up --build
```

---

### 🧪 Endpoints

| Service   | URL                     |
|-----------|--------------------------|
| Backend   | http://localhost:8000    |
| Frontend  | http://localhost:3000    |
| Health    | http://localhost:8000/health |

---

### 📄 Notes
- Backend logs trades to `backend/logs/trades_log.jsonl`
- Frontend auto-refreshes on changes via volume mount