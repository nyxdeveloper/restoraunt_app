# django
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import User


class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm):
        model = User
        fields = (
            "phone",
            "name",
            "username",
            "password",
            "is_staff",
            "is_superuser",
            "is_active"
        )


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = (
            "phone",
            "name",
            "username",
            "password",
            "points",
            "is_staff",
            "is_superuser",
            "is_active",
        )
