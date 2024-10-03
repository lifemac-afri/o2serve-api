import uuid
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models
from django.contrib import admin  # Add this import

class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    role = models.CharField(max_length=10, choices=(('admin', 'Admin'), ('waiter', 'Waiter'), ('superadmin', 'Superadmin')))
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    groups = models.ManyToManyField(
        Group,
        related_name='custom_user_set',  # Change this to a unique name
        blank=True,
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='custom_user_permissions_set',  # Change this to a unique name
        blank=True,
    )


