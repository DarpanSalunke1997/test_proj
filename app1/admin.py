from django.contrib import admin

# Register your models here.
from .models import NewModel

admin.site.register(NewModel)
