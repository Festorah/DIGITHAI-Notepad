from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.utils.translation import gettext_lazy as _

from .object_event_tracker import ObjectEventTracker
from .uuid_primary_key import UUIDPrimaryKey


class UserManager(BaseUserManager):
    """
    User account manager for a user model. The user's email address will be used in place of the username
    """

    use_in_migrations = True

    def _create_user(self, email_address, password, **extra_fields):
        """
        Create and save a user with the supplied email and password
        """
        email_address = self.normalize_email(email_address)

        user = self.model(email_address=email_address, **extra_fields)
        user.set_password(password or None)
        user.save(using=self._db)
        return user

    def create_user(self, email_address: str, password: str, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        extra_fields.setdefault("is_active", True)

        user = self._create_user(email_address, password, **extra_fields)

        return user

    def create_superuser(self, email_address: str, password: str, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        user = self._create_user(email_address, password, **extra_fields)

        return user


class AccountUser(UUIDPrimaryKey, ObjectEventTracker, AbstractUser):

    email = None
    username = None

    email_address = models.EmailField(_("email address"), max_length=100, unique=True)
    is_active = models.BooleanField(_("active status"), default=True)
    first_name = models.CharField(
        _("first name"), max_length=150, blank=True, default="", editable=False
    )
    last_name = models.CharField(
        _("first name"), max_length=150, blank=True, default="", editable=False
    )

    USERNAME_FIELD = "email_address"
    REQUIRED_FIELDS = []

    objects = UserManager()

    class Meta:
        verbose_name = _("user")
        verbose_name_plural = _("users")
        ordering = ("-date_joined",)
        indexes = [
            models.Index(fields=["email_address"]),
        ]

    @property
    def name(self):
        name = f"{self.first_name}"
        if self.last_name:
            name += f" {self.last_name}"
        return name

    @property
    def full_name(self):
        return self.name

    def get_full_name(self):
        return self.name

    def delete(self, *args, **kwargs):
        deleted = super().delete(*args, **kwargs)
        return deleted
