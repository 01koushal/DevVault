from rest_framework import viewsets, decorators, response, status, permissions
from .models import Secret
from .serializers import SecretSerializer

class SecretViewSet(viewsets.ModelViewSet):
    serializer_class = SecretSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Secret.objects.filter(owner=self.request.user)

    @decorators.action(detail=True, methods=["post"])
    def reveal(self, request, pk=None):
        secret = self.get_object()
        return response.Response({"id": secret.id, "name": secret.name, "secret_value": secret.get_value()})
