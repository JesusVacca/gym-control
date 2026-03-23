from django.db import models

class SaleTask(models.Model):
    name = models.CharField(max_length=100)
    amount = models.PositiveIntegerField(default=0)
    description = models.TextField()
    is_done = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('-created_at',)
        verbose_name = 'Tarea'
        verbose_name_plural = 'Tareas'
