from django.contrib import admin
from .models import newsColumn_info, newsArticle_info, weekbook_info, booktop_info

class newsColumnAdmin(admin.ModelAdmin):
    list_display = ('columnName','columnSlug', 'abstract', 'nav_display')

class newsArticleAdmin(admin.ModelAdmin):
    list_display = ('newsTitle', 'newsColumn', 'newsAuthor', 'newsPubdate', 'newsPublished')

class RecbookAdmin(admin.ModelAdmin):
    list_display = ('bookName', 'recTime', 'promugator', 'now_display', 'past_display')

class RankAdmin(admin.ModelAdmin):
    list_display = ('number', 'bookName', 'bookAuthor', 'pub_display')

admin.site.register(weekbook_info, RecbookAdmin)
admin.site.register(newsColumn_info, newsColumnAdmin)
admin.site.register(newsArticle_info, newsArticleAdmin)
admin.site.register(booktop_info, RankAdmin)