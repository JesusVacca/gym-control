from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
# Create your models here.


class BaseMemberManager(BaseUserManager):
    def create_member(self, first_name, email, password = None, **extra_fields):
        if not email:
            raise ValueError("Email cannot be None")
        if not extra_fields.get('phone_number'):
            raise ValueError("Phone number cannot be None")

        email = self.normalize_email(email)
        instance = self.model(
            first_name = first_name,
            email = email,
            **extra_fields
        )
        instance.set_password(password)
        instance.save(using = self._db)
        return instance

    def create_superuser(self, first_name, email, password = None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('role', Member.BaseRoles.ADMINISTRATOR)
        return self.create_member(first_name, email, password, **extra_fields)


class Member(AbstractBaseUser):

    class BaseRoles(models.TextChoices):
        CUSTOMER = 'Cliente','Cliente'
        ADMINISTRATOR = 'Administrador','Administrador'
        SECRETARY = 'Secretario(a)','Secretario(a)'

    objects = BaseMemberManager()
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100, blank=True, null=True)
    phone_number = models.CharField(max_length=10)
    email = models.EmailField(unique=True, db_index=True)
    role = models.CharField(max_length=13, choices=BaseRoles.choices, default=BaseRoles.CUSTOMER)
    weight = models.DecimalField(max_digits=5, decimal_places=2)
    height = models.DecimalField(max_digits=5, decimal_places=2)
    photo = models.ImageField(upload_to='members/images',)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    birthday = models.DateField(blank=True, null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'phone_number', 'weight', 'height']

