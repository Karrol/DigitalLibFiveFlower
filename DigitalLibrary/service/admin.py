from django.contrib import admin
from .models import Category, Intro

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('categoryName',  'side_display')
    list_filter = ['side_display']


class IntroAdmin(admin.ModelAdmin):
    list_display = ('serviceTitle', 'serviceAuthor', 'servicePublished', 'servicePubdate')
    list_filter = ['servicePublished', 'servicePubdate']
    raw_id_fields = ("serviceAuthor",)

admin.site.register(Category, CategoryAdmin)
admin.site.register(Intro, IntroAdmin)