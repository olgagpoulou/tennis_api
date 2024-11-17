from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models

# Δημιουργία του Custom User Manager
class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Το πεδίο email πρέπει να είναι καταχωρημένο.')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)  # Χρησιμοποιούμε την έτοιμη μέθοδο του Django για τον κωδικό
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(email, password, **extra_fields)

# Ορισμός του προσαρμοσμένου μοντέλου χρήστη
class User(AbstractUser):
    name = models.CharField(max_length=255)
    email = models.CharField(max_length=255, unique=True)
    username = None  # Δεν χρειάζεται πεδίο για username
    USERNAME_FIELD = 'email'  # Χρησιμοποιούμε το email ως username
    REQUIRED_FIELDS = []  # Δεν απαιτείται το username

    objects = CustomUserManager()  # Ορίζουμε τον Custom User Manager
