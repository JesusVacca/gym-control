from django.contrib import admin
from apps.sales.models import Income,CashOpening, SaleTask
# Register your models here.
admin.site.register(Income)
admin.site.register(CashOpening)
admin.site.register(SaleTask)
