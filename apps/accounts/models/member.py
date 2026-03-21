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
    class Meta:
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'

    class BaseRoles(models.TextChoices):
        CUSTOMER = 'Cliente','Cliente'
        ADMINISTRATOR = 'Administrador','Administrador'
        SECRETARY = 'Secretario(a)','Secretario(a)'

    class DocumentTypes(models.TextChoices):
        CC = 'CC', 'Cédula de Ciudadanía'
        TI = 'TI', 'Tarjeta de Identidad'
        CE = 'CE', 'Cédula de Extranjería'
        NIT = 'NIT', 'Número de Identificación Tributaria'
        PP = 'PP', 'Pasaporte'
        RC = 'RC', 'Registro Civil'
        PPT = 'PPT', 'Permiso por Protección Temporal'

    objects = BaseMemberManager()
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100, blank=True, null=True)
    phone_number = models.CharField(max_length=10, unique=True, db_index=True)
    email = models.EmailField(unique=True, db_index=True)
    role = models.CharField(max_length=13, choices=BaseRoles.choices, default=BaseRoles.CUSTOMER)
    photo = models.ImageField(upload_to='members/images', blank=True, null=True)
    document_type = models.CharField(max_length=100, choices=DocumentTypes.choices, default=DocumentTypes.CC)
    document_number = models.PositiveIntegerField(unique=True, db_index=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    birthday = models.DateField(blank=True, null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'phone_number','document_type','document_number']


    def delete_image(self):
        import os
        if self.photo:
            try:
                if os.path.exists(self.photo.path):
                    os.remove(self.photo.path)
                    return True
            except FileNotFoundError:...
        return False


    @property
    def full_name(self):
        return f'{self.first_name} {self.last_name if self.last_name else ""}'

    def has_perm(self, perm, obj=None):
        return self.is_superuser or self.is_staff

    def has_module_perms(self, app_label):
        return self.is_superuser or self.is_staff

    def __str__(self):
        return f'{self.full_name} - {self.phone_number}'

