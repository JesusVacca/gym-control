from django.contrib import admin
from apps.memberships.models import Membership, Plan

# Register your models here.

admin.site.register(Membership)
admin.site.register(Plan)