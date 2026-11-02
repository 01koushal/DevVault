from rest_framework import serializers
from .models import Secret

class SecretSerializer(serializers.ModelSerializer):
    secret_value = serializers.CharField(write_only=True, required=False, allow_blank=False)
    masked_value = serializers.SerializerMethodField()

    class Meta:
        model = Secret
        fields = ["id", "name", "project", "secret_type", "secret_value", "masked_value", "notes", "created_at", "updated_at"]
        read_only_fields = ["id", "masked_value", "created_at", "updated_at"]

    def get_masked_value(self, obj):
        return "••••••••••••"

    def create(self, validated_data):
        value = validated_data.pop("secret_value")
        request = self.context["request"]
        secret = Secret(owner=request.user, **validated_data)
        secret.set_value(value)
        secret.save()
        return secret

    def update(self, instance, validated_data):
        value = validated_data.pop("secret_value", None)
        for key, value_item in validated_data.items():
            setattr(instance, key, value_item)
        if value is not None:
            instance.set_value(value)
        instance.save()
        return instance
