from django.db import models
from django.db.models import Sum



class CashOpening(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    team = models.ForeignKey('accounts.Member', on_delete=models.PROTECT, related_name='cash_opening_team')
    amount = models.PositiveIntegerField()
    is_open = models.BooleanField(default=True, db_index=True)



    @property
    def total_day(self):
        return self.income_cash_opening\
            .aggregate(total_day = Sum('amount'))['total_day'] or 0

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Apertura de caja'
        verbose_name_plural = 'Aperturas de caja'
