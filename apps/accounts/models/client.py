from django.db import models
from .member import Member

class ClientManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(
            role=Member.BaseRoles.CUSTOMER
        ).order_by("-created_at")


class Client(Member):
    objects = ClientManager()

    class Meta:
        proxy = True
        verbose_name = 'Cliente'
        verbose_name_plural = 'Clientes'