from django.contrib import admin
from .models import Category, Intro

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('categoryName',  'side_display')


class IntroAdmin(admin.ModelAdmin):
    list_display = ('serviceTitle', 'serviceAuthor', 'servicePublished', 'servicePubdate')

admin.site.register(Category, CategoryAdmin)
admin.site.register(Intro, IntroAdmin)