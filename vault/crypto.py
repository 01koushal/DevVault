import os
from pathlib import Path
from cryptography.fernet import Fernet, InvalidToken
from django.conf import settings

BASE_DIR = Path(settings.BASE_DIR)
KEY_FILE = BASE_DIR / "devvault.key"

def _get_fernet():
    key = os.environ.get("DEVAULT_ENCRYPTION_KEY", "").strip()
    if not key:
        if KEY_FILE.exists():
            key = KEY_FILE.read_text(encoding="utf-8").strip()
        else:
            key = Fernet.generate_key().decode("utf-8")
            KEY_FILE.write_text(key, encoding="utf-8")
            try:
                KEY_FILE.chmod(0o600)
            except OSError:
                pass
    try:
        return Fernet(key.encode("utf-8"))
    except (ValueError, TypeError) as exc:
        raise RuntimeError("DEVAULT_ENCRYPTION_KEY is invalid. Generate a Fernet key and set it privately.") from exc

def encrypt_value(value: str) -> str:
    return _get_fernet().encrypt(value.encode("utf-8")).decode("utf-8")

def decrypt_value(value: str) -> str:
    try:
        return _get_fernet().decrypt(value.encode("utf-8")).decode("utf-8")
    except InvalidToken as exc:
        raise RuntimeError("Cannot decrypt this secret. Check that the original DevVault encryption key is available.") from exc
