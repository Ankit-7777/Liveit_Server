from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils.translation import gettext_lazy as _
from django.core.validators import RegexValidator
from django.core.validators import FileExtensionValidator
from .base import BaseModel

class MyUserManager(BaseUserManager):
    def create_user(self, phone, password=None, **extra_fields):
        if not phone:
            raise ValueError('The Phone field must be set')
        user = self.model(phone=phone, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(phone, password=password, **extra_fields)

class UserProfile(AbstractBaseUser, PermissionsMixin, BaseModel):
    email = models.EmailField(verbose_name="Email", max_length=255, unique=True, blank=True, null=True)
    username = models.CharField(_("Full Name"), max_length=255)
    image = models.ImageField(_("Image"), upload_to='ProfileImages/', blank=True, null=True, validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png', 'webp'])])
    phone = models.CharField(_("Phone"), max_length=13, unique=True,)
    occasion_name = models.CharField(_("Occasion Name"), max_length=100, blank=True, null=True)
    dob = models.DateField(_("Date of birth"), blank=True, null=True,)
    is_verified = models.BooleanField(_("verified"), default= False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=True)
   

    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = ['username']

    objects = MyUserManager()

    def __str__(self):
        return self.username


