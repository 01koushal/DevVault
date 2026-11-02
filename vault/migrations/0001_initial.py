# Generated for DevVault
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models
import django.utils.timezone

class Migration(migrations.Migration):
    initial = True
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]
    operations = [
        migrations.CreateModel(
            name="Secret",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=120)),
                ("project", models.CharField(default="Personal", max_length=100)),
                ("secret_type", models.CharField(choices=[("API Key", "API Key"), ("Access Token", "Access Token"), ("Database", "Database"), ("Password", "Password"), ("Other", "Other")], default="API Key", max_length=30)),
                ("encrypted_value", models.TextField()),
                ("notes", models.TextField(blank=True)),
                ("created_at", models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("owner", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="secrets", to=settings.AUTH_USER_MODEL)),
            ],
            options={"ordering": ["-updated_at"]},
        ),
        migrations.AddIndex(
            model_name="secret",
            index=models.Index(fields=["owner", "project"], name="vault_secret_owner_i_3f0c1a_idx"),
        ),
    ]
