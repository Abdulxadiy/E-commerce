from django.contrib.auth.models import AbstractUser, PermissionsMixin, BaseUserManager
from typing import Any, ClassVar

class CustomUserManager(BaseUserManager):
    def create(self, **kwargs: Any) -> CustomUser: ...
    def create_user(
        self, phone_number: str, password: str | None = None, **extra_fields: Any
    ) -> CustomUser: ...
    def create_superuser(
        self, phone_number: str, password: str | None = None, **extra_fields: Any
    ) -> CustomUser: ...

class CustomUser(AbstractUser, PermissionsMixin):
    phone_number: str
    data_joined: Any
    is_active: bool
    is_staff: bool

    objects: ClassVar[CustomUserManager]

    USERNAME_FIELD: str
    REQUIRED_FIELDS: list[str]

    def __str__(self) -> str: ...

