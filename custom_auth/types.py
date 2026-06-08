from typing import Type, cast
from django.contrib.auth import get_user_model
from .models import CustomUser

# Centralized typed alias for the project to use everywhere.
# Use `from custom_auth.types import User` in tests/views/serializers.
User: Type[CustomUser] = cast(Type[CustomUser], get_user_model())

