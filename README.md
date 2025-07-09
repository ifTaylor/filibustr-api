# 🏛️ Filibustr API

This is the backend service for the **Filibustr** civic engagement app.  
It parses active congressional bills and serves them to the frontend.

## 🔧 Stack

- Python 3.10+
- FastAPI
- Uvicorn
- Requests (for ProPublica Congress API)
- dotenv

## 📦 Run Locally

```bash
poetry install
& "C:\Program Files\PostgreSQL\17\bin\pg_ctl.exe" start -D "C:\Program Files\PostgreSQL\17\data"
poetry run uvicorn main:app --reload
