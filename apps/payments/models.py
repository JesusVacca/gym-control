from django.db import models
from django.db.models import Sum



class Payment(models.Model):

    class PaymentMethod(models.TextChoices):
        CASH = 'Efectivo', 'Efectivo'
        TRANSFER = 'Transferencia', 'Transferencia'


    class PaymentType(models.TextChoices):
        DAY_PASS = 'Pase de un día','Pase de un día'
        MEMBERSHIP = 'Membresía','Membresía'

    payment_type = models.CharField(max_length=20, choices=PaymentType.choices, default=PaymentType.DAY_PASS, editable=False)
    payment_method = models.CharField(max_length=20, choices=PaymentMethod.choices, default=PaymentMethod.CASH)
    membership = models.ForeignKey('memberships.Membership', on_delete=models.PROTECT, related_name='payments', blank=True, null=True)
    amount = models.PositiveIntegerField()
    payment_date = models.DateTimeField(auto_now_add=True)

    @property
    def payment_owner(self):
        return self.membership.member.full_name if self.membership else self.payment_type

    @property
    def total_paid(self):
        return Payment\
            .objects\
            .filter(membership=self.membership)\
            .aggregate(total=Sum('amount'))['total'] or 0

    @property
    def debt(self):return self.membership.price - self.total_paid if self.membership else 0


    def save(self, *args, **kwargs):
        if not self.membership:
            self.payment_type = Payment.PaymentType.DAY_PASS
        else:
            self.payment_type = Payment.PaymentType.MEMBERSHIP
        super().save(*args, **kwargs)

    class Meta:
        ordering = ['-payment_date']
        verbose_name = 'Pago'
        verbose_name_plural = 'Pagos'
