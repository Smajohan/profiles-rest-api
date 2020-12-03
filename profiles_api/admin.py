from django.contrib import admin

from profiles_api import models


# Register your models here.
admin.site.register(models.UserProfile) # Tells the Django admin to register the user profile model with the admin site -> accessible through the admin interface
