from django.urls import path
from . import views

urlpatterns = [
    path("", views.dashboard, name="dashboard"),
    path("login/", views.login_view, name="login"),
    path("register/", views.register_view, name="register"),
    path("logout/", views.logout_view, name="logout"),
    path("secrets/new/", views.secret_create, name="secret_create"),
    path("secrets/<int:pk>/edit/", views.secret_edit, name="secret_edit"),
    path("secrets/<int:pk>/delete/", views.secret_delete, name="secret_delete"),
    path("secrets/<int:pk>/reveal/", views.secret_reveal, name="secret_reveal"),
]
