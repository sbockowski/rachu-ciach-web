# apps/savings/admin.py
from django.contrib import admin
from .models import SavingsSnapshot

admin.site.register(SavingsSnapshot)