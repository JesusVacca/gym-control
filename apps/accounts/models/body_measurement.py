from django.db import models

class BodyMeasurement(models.Model):
    client = models.ForeignKey('accounts.Client', on_delete=models.PROTECT, related_name='body_measurement')
    weight = models.DecimalField(max_digits=10, decimal_places=2)
    biceps = models.DecimalField(max_digits=10, decimal_places=2)
    chest = models.DecimalField(max_digits=10, decimal_places=2)
    high_abdomen = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    mid_abdomen = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    lower_abdomen = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    tail = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    leg = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    adductor = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    calf = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return str(self.client.first_name if self.client else "")
