from django.db import models

# Create your models here.

class AppSettings(models.Model):
    app_name = models.CharField(max_length=100, default="Gimnasio")
    app_description = models.CharField(max_length=200, default="Panel de administración")
    app_image = models.ImageField(upload_to="management/images/", null=True, blank=True)
    app_logo = models.ImageField(upload_to="management/images/", null=True, blank=True)
    elements_per_section = models.PositiveIntegerField(default=10)

    @classmethod
    def load(cls):
        instance, _ = cls.objects.get_or_create(pk=1)
        return instance
    
    def save(self, *args, **kwargs):
        try:
            old_instance = AppSettings.objects.get(pk=self.pk)
            if old_instance.app_logo and old_instance.app_logo != self.app_logo:
                old_instance.app_logo.delete(save=False)
            if old_instance.app_image and old_instance.app_image != self.app_image:
                old_instance.app_image.delete(save=False)
        except AppSettings.DoesNotExist:...
        super().save(*args, **kwargs)