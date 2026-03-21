from django.contrib import admin
from apps.accounts.models import Member, Client, BodyMeasurement

# Register your models here.

admin.site.register(Member)
admin.site.register(Client)
admin.site.register(BodyMeasurement)
