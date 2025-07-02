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
poetry run uvicorn main:app --reload
