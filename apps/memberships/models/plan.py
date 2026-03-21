from django.db import models

class Plan(models.Model):
    name = models.CharField(max_length=100, unique=True, db_index=True)
    duration_days = models.PositiveIntegerField()
    price = models.PositiveIntegerField()
    description = models.TextField(blank=True)

    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    @property
    def status(self):
        return 'Activo' if self.is_active else 'Inactivo'

    class Meta:
        ordering = ['price']