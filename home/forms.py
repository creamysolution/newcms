# forms.py
# Note: templates use {{ form.field }} directly, so each widget needs
# Bootstrap's "form-control" class added via widget attrs — otherwise
# Django renders a plain, unstyled <input>.

from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Event
from tinymce.widgets import TinyMCE

INPUT_CLASS = "form-control"


class RegisterForm(UserCreationForm):
    full_name = forms.CharField(max_length=100, widget=forms.TextInput(
        attrs={"class": INPUT_CLASS, "placeholder": "Jane Doe"}))
    email = forms.EmailField(widget=forms.EmailInput(
        attrs={"class": INPUT_CLASS, "placeholder": "jane@example.com"}))

    class Meta:
        model = User
        fields = ["full_name", "username", "email", "password1", "password2"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username"].widget.attrs.update(
            {"class": INPUT_CLASS, "placeholder": "janedoe"})
        self.fields["password1"].widget.attrs.update(
            {"class": INPUT_CLASS, "placeholder": "••••••••"})
        self.fields["password2"].widget.attrs.update(
            {"class": INPUT_CLASS, "placeholder": "••••••••"})


class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(
        attrs={"class": INPUT_CLASS, "placeholder": "janedoe"}))
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={"class": INPUT_CLASS, "placeholder": "••••••••"}))

from django.utils import timezone
class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ["name", "description", "dnt", "venue", "total_seats"]
        widgets = {
            "name": forms.TextInput(attrs={
                "class": INPUT_CLASS, "placeholder": "Django Basics Workshop"}),
            "dnt": forms.DateTimeInput(attrs={
                "class": INPUT_CLASS, "type": "datetime-local"}),
            "venue": forms.TextInput(attrs={
                "class": INPUT_CLASS, "placeholder": "Community Hall, Kathmandu"}),
            "total_seats": forms.NumberInput(attrs={
                "class": INPUT_CLASS, "min": 1, "placeholder": "50"}),
        }


    def is_valid(self):
        valid = super().is_valid()
        if not valid:
            return valid

        # Ensure the event date is in the future
        dnt = self.cleaned_data.get("dnt")
        if dnt and dnt <= timezone.now():
            self.add_error("dnt", "Event date and time must be in the future.")
            return False

        return True
