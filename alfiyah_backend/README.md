# Alfiyah Backend API

## Requirements
- Python 3.10+
- MySQL (Laragon) with database named `alfiyah_db`

## Setup

```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS/Linux
source .venv/bin/activate

pip install -r requirements.txt
```

## Environment

The default database URL is configured for Laragon:

```
mysql+pymysql://root@localhost/alfiyah_db
```

To override settings, set environment variables before running:

```bash
set DATABASE_URL=mysql+pymysql://root@localhost/alfiyah_db
set SECRET_KEY=your-secret

# macOS/Linux
export DATABASE_URL=mysql+pymysql://root@localhost/alfiyah_db
export SECRET_KEY=your-secret
```

## Run the API

```bash
uvicorn app.main:app --reload
```

Swagger UI: http://localhost:8000/docs

## Seed initial data

```bash
python seed_data.py
```
