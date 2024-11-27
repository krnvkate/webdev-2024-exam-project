from django.contrib import admin

from .models import Profile, FavoriteRecipe

admin.site.register(Profile)
admin.site.register(FavoriteRecipe)

