from django.utils import timezone
from django.db import models

# Create your models here.

class Attendance(models.Model):
    client = models.ForeignKey('accounts.Client', on_delete=models.PROTECT, related_name='attendances')
    check_in = models.DateTimeField(default=timezone.now)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.client.first_name} - {self.check_in} '

    class Meta:
        ordering = ('-check_in',)
        verbose_name = 'Gestión de asistencia'
        verbose_name_plural = 'Gestión de asistencias'