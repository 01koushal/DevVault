from django.contrib import admin
from .models import Secret

@admin.register(Secret)
class SecretAdmin(admin.ModelAdmin):
    list_display = ("name", "project", "secret_type", "owner", "updated_at")
    list_filter = ("secret_type", "project")
    search_fields = ("name", "project", "owner__username")
    readonly_fields = ("encrypted_value",)
