# agent-zero-trust v2 web app

Experimental browser questionnaire for the `agent-zero-trust` scanner.

## Backend

```bash
pip install -e ".[web,dev]"
uvicorn web.backend.app:app --reload --host 127.0.0.1 --port 8000
```

Endpoints:

- `GET /health`
- `POST /scan`
- `POST /reports/markdown`
- `POST /reports/json`

## Frontend

```bash
cd web/frontend
npm install
npm run dev
```

Open `http://127.0.0.1:5173`.
