from django import forms
from .models import Secret

class SecretForm(forms.ModelForm):
    secret_value = forms.CharField(
        label="Secret value",
        widget=forms.Textarea(attrs={"rows": 3, "autocomplete": "off", "placeholder": "Paste a demo credential"}),
        help_text="Encrypted before storage. Use fake/demo credentials for testing."
    )
    class Meta:
        model = Secret
        fields = ["name", "project", "secret_type", "notes"]
        widgets = {
            "name": forms.TextInput(attrs={"placeholder": "e.g. Stripe test key"}),
            "project": forms.TextInput(attrs={"placeholder": "e.g. Portfolio app"}),
            "notes": forms.Textarea(attrs={"rows": 2, "placeholder": "Optional context"}),
        }
    def __init__(self, *args, **kwargs):
        self.instance_value = kwargs.pop("instance_value", None)
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.setdefault("class", "input")
        self.fields["secret_type"].widget.attrs["class"] = "input"
