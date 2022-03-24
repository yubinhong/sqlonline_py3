from django.contrib import admin

# Register your models here.
from web import models
admin.site.register(models.Product)
admin.site.register(models.UserProfile)
admin.site.register(models.SecretDB)