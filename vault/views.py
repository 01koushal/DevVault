from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST
from .forms import SecretForm
from .models import Secret

def login_view(request):
    if request.user.is_authenticated:
        return redirect("dashboard")
    form = AuthenticationForm(request, data=request.POST or None)
    if request.method == "POST" and form.is_valid():
        login(request, form.get_user())
        return redirect("dashboard")
    return render(request, "vault/login.html", {"form": form})

def register_view(request):
    if request.user.is_authenticated:
        return redirect("dashboard")
    form = UserCreationForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        user = form.save()
        login(request, user)
        return redirect("dashboard")
    return render(request, "vault/register.html", {"form": form})

@login_required
def dashboard(request):
    qs = Secret.objects.filter(owner=request.user)
    query = request.GET.get("q", "").strip()
    project = request.GET.get("project", "").strip()
    if query:
        qs = qs.filter(name__icontains=query) | qs.filter(project__icontains=query)
    if project:
        qs = qs.filter(project__iexact=project)
    secrets_list = list(qs.distinct())
    projects = list(Secret.objects.filter(owner=request.user).values_list("project", flat=True).distinct())
    context = {
        "secrets": secrets_list,
        "total_count": Secret.objects.filter(owner=request.user).count(),
        "project_count": len(projects),
        "project_names": projects,
        "query": query,
        "selected_project": project,
    }
    return render(request, "vault/dashboard.html", context)

@login_required
def secret_create(request):
    form = SecretForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        secret = form.save(commit=False)
        secret.owner = request.user
        secret.set_value(form.cleaned_data["secret_value"])
        secret.save()
        messages.success(request, "Secret encrypted and saved.")
        return redirect("dashboard")
    return render(request, "vault/secret_form.html", {"form": form, "page_title": "Add a secret"})

@login_required
def secret_edit(request, pk):
    secret = get_object_or_404(Secret, pk=pk, owner=request.user)
    form = SecretForm(request.POST or None, instance=secret)
    if request.method == "POST" and form.is_valid():
        secret = form.save(commit=False)
        secret.set_value(form.cleaned_data["secret_value"])
        secret.save()
        messages.success(request, "Secret updated.")
        return redirect("dashboard")
    return render(request, "vault/secret_form.html", {"form": form, "page_title": "Edit secret"})

@login_required
@require_POST
def secret_delete(request, pk):
    secret = get_object_or_404(Secret, pk=pk, owner=request.user)
    secret.delete()
    messages.success(request, "Secret deleted.")
    return redirect("dashboard")

@login_required
def secret_reveal(request, pk):
    secret = get_object_or_404(Secret, pk=pk, owner=request.user)
    return render(request, "vault/reveal.html", {"secret": secret, "value": secret.get_value()})

def logout_view(request):
    from django.contrib.auth import logout
    if request.method == "POST":
        logout(request)
        return redirect("login")
    return redirect("dashboard")
