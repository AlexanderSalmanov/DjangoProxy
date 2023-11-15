from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)


class UserManager(BaseUserManager):
    def create_user(self, email, password, **extra_args):
        """Creates and saves a new user"""
        if not email:
            raise ValueError("Users must have an email address")
        if not password:
            raise ValueError("Users must have a password")
        user = self.model(email=self.normalize_email(email), **extra_args)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password, **extra_args):
        extra_args.setdefault("is_staff", True)
        extra_args.setdefault("is_superuser", True)

        return self.create_user(email, password, **extra_args)


class User(AbstractBaseUser):
    email = models.CharField(max_length=255, unique=True)
    full_name = models.CharField(max_length=255, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = "email"

    objects = UserManager()

    def __str__(self):
        return self.email

    def get_full_name(self):
        return self.full_name if self.full_name else "Anonymous"

    def get_short_name(self):
        if self.full_name:
            if len(self.full_name).split() > 1:
                return self.full_name.split()[0]
            return self.full_name
        return "Anonymous"

    def has_perm(self, perm, obj=None):
        return self.is_superuser

    def has_module_perms(self, app_label):
        return self.is_superuser
