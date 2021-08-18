from django.contrib import admin
from .models import ActiveHour, Doctor

admin.site.register(Doctor)
admin.site.register(ActiveHour)
# Register your models here.