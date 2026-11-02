from rest_framework.routers import DefaultRouter
from .api_views import SecretViewSet

router = DefaultRouter()
router.register("secrets", SecretViewSet, basename="secret")
urlpatterns = router.urls
