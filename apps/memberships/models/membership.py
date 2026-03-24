from datetime import timedelta

from django.db import models
from django.utils import timezone


class Membership(models.Model):
    class Status(models.TextChoices):
        ACTIVE = "Activa", "Activa"
        EXPIRED = "Vencida", "Vencida"
        FROZEN = "Congelada", "Congelada"
        CANCELLED = "Cancelada", "Cancelada"

    plan = models.ForeignKey('memberships.Plan', on_delete=models.PROTECT, related_name='memberships')
    member = models.ForeignKey('accounts.Client', on_delete=models.PROTECT, related_name='memberships')
    status = models.CharField(
        max_length=20,
        choices=Status,
        default=Status.ACTIVE,
    )
    start_date = models.DateField(default=timezone.now)
    end_date = models.DateField()
    price = models.PositiveIntegerField()
    notified_expiration = models.BooleanField(default=False)
    frozen_until = models.DateField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.plan.name} - {self.member.first_name} - Debe: {str(self.debt)}'



    @property
    def is_paid(self):
        return self.debt == 0

    @property
    def debt(self):
        if hasattr(self, 'total_paid'):
            return max(self.price - self.total_paid, 0)
        total_paid = self.payments.aggregate(
            total=models.Sum('amount')
        )['total'] or 0
        return max(self.price - total_paid, 0)

    def save(self, *args, **kwargs):
        start_date = self.start_date or timezone.now()
        self.end_date = start_date + timedelta(days=self.plan.duration_days - 1)
        self.price = self.plan.price
        super().save(*args, **kwargs)

    class Meta:
        ordering = ('-created_at',)