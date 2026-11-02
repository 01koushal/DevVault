from django.conf import settings
from django.db import models
from django.utils import timezone
from .crypto import encrypt_value, decrypt_value

class Secret(models.Model):
    SECRET_TYPES = [
        ("API Key", "API Key"),
        ("Access Token", "Access Token"),
        ("Database", "Database"),
        ("Password", "Password"),
        ("Other", "Other"),
    ]
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="secrets")
    name = models.CharField(max_length=120)
    project = models.CharField(max_length=100, default="Personal")
    secret_type = models.CharField(max_length=30, choices=SECRET_TYPES, default="API Key")
    encrypted_value = models.TextField()
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(default=timezone.now, editable=False)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-updated_at"]
        indexes = [models.Index(fields=["owner", "project"])]

    def set_value(self, raw_value: str):
        self.encrypted_value = encrypt_value(raw_value)

    def get_value(self) -> str:
        return decrypt_value(self.encrypted_value)

    def __str__(self):
        return f"{self.name} ({self.project})"
