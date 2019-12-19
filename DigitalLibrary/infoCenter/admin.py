from django.contrib import admin
from .models import newsColumn_info, newsArticle_info, weekbook_info

class newsColumnAdmin(admin.ModelAdmin):
    list_display = ('columnName','columnSlug', 'abstract', 'nav_display')

class newsArticleAdmin(admin.ModelAdmin):
    list_display = ('newsTitle', 'newsColumn', 'newsAuthor', 'newsPubdate', 'newsPublished')

class RecbookAdmin(admin.ModelAdmin):
    raw_id_fields = ("ISBN",)
    list_display = ('bookName', 'recTime', 'promugator', 'index_display')

admin.site.register(weekbook_info, RecbookAdmin)
admin.site.register(newsColumn_info, newsColumnAdmin)
admin.site.register(newsArticle_info, newsArticleAdmin)