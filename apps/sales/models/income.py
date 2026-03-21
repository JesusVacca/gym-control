from django.db import models

class Income(models.Model):
    class Source(models.TextChoices):
        SALES = 'VENTAS','VENTAS'
        PAYMENT = 'PAGOS','PAGOS'
        MANUAL = 'MANUAL','MANUAL'

    class IncomeCategory(models.TextChoices):
        GYM = 'GYM','GYM'
        REFRIGERATOR = 'NEVERA','NEVERA'
        COFFEE = 'CAFÉ', 'CAFÉ'
        HERBALIFE = 'HERBALIFE','HERBALIFE'
        PROTEIN = 'PROTEINA', 'PROTEINA'

    class IncomeMethod(models.TextChoices):
        CASH = 'Efectivo', 'Efectivo'
        TRANSFER = 'Transferencia', 'Transferencia'

    category = models.CharField(max_length=20, choices=IncomeCategory.choices)
    amount = models.PositiveIntegerField()
    payment_method = models.CharField(max_length=20, choices=IncomeMethod.choices)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    cash_opening = models.ForeignKey('sales.CashOpening', on_delete=models.PROTECT, related_name='income_cash_opening', null=True, blank=True, editable=False)
    source = models.CharField(max_length=10, choices=Source.choices)
    payment = models.OneToOneField('payments.Payment', on_delete=models.PROTECT, related_name='payments', editable=False, blank=True, null=True)


    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Ingreso'
        verbose_name_plural = 'Ingresos'