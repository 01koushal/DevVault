# DevVault — Django Secrets Manager

A portfolio-ready local Django app for organizing API keys and application secrets. Includes authentication, a dark dashboard, encrypted secret values, project labels, search, and a small authenticated REST API.

## Requirements
- Python 3.10+
- pip

SQLite is configured by default; no database server is required.

## Windows quick start
```bat
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```
Open http://127.0.0.1:8000/ and sign in with the superuser credentials you created.

## First-time setup
1. Copy `.env.example` to `.env` (optional for local use).
2. Generate an encryption key:
   ```bat
   python -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"
   ```
3. Set `DEVAULT_ENCRYPTION_KEY` in your environment before running the server. If you don't set it, DevVault creates a local key in `devvault.key` on first run. **Keep this key private and back it up**: encrypted values cannot be recovered without it.
4. Create a superuser as above. Sign in to the dashboard.
5. Add a secret using the form. Secret values are encrypted before being stored.

## REST API
All endpoints require Django session authentication and CSRF protection by default. Sign in to the web UI first or use a client that supports Django session auth.

- `GET /api/secrets/` — list your secret metadata (secret values are not returned by default)
- `POST /api/secrets/` — create a secret (`name`, `project`, `secret_type`, `secret_value`, optional `notes`)
- `GET /api/secrets/<id>/` — retrieve metadata
- `PATCH /api/secrets/<id>/` — update metadata or secret value
- `DELETE /api/secrets/<id>/` — delete a secret
- `POST /api/secrets/<id>/reveal/` — decrypt and return the value to the authenticated owner only

Example create JSON:
```json
{
  "name": "Demo API token",
  "project": "Portfolio",
  "secret_type": "API Key",
  "secret_value": "replace-with-a-fake-test-value",
  "notes": "Local demo only"
}
```

## Security notes
- This is an educational portfolio project, not a production-grade password manager.
- Use a strong, privately stored encryption key; do not commit it to Git.
- Use HTTPS and secure deployment settings before exposing it publicly.
- The reveal endpoint intentionally returns plaintext only on explicit authenticated request.
- Use fake/demo credentials for screenshots and testing. Never upload real credentials to a public demo.
