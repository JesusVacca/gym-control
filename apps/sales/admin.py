from django.contrib import admin
from apps.sales.models import Income,CashOpening
# Register your models here.

class IncomeAdmin(admin.ModelAdmin):
    list_filter = ('created_at',)


admin.site.register(Income, IncomeAdmin)
admin.site.register(CashOpening)
